#!/usr/bin/env python3
"""
Gmail Email Manager Script
Read, summarize, reply to, and send emails via Gmail API.

Setup (first time):
  1. Get credentials.json from Google Cloud Console (Gmail API)
  2. Place it in data/credentials.json
  3. Run: python email_manager.py --auth

Usage:
  python email_manager.py --action list --limit 10
  python email_manager.py --action read --id <email_id>
  python email_manager.py --action reply --id <email_id> --body "Your reply"
  python email_manager.py --action send --to "email@example.com" --subject "Subject" --body "Body"
"""

import argparse
import base64
import json
import os
import sys
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

# ─── Try imports ─────────────────────────────────────────────────────────────
missing = []
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    missing.append("google-api-python-client google-auth-oauthlib google-auth-httplib2")

if missing:
    print(f"ERROR: Missing packages. Run: pip install {' '.join(missing)}")
    sys.exit(1)

# ─── Config ─────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent
CREDENTIALS_FILE = PROJECT_ROOT / "data" / "credentials.json"
TOKEN_FILE = Path.home() / ".openclaw" / "gmail_token.json"

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
]


# ─── Auth ────────────────────────────────────────────────────────────────────
def get_gmail_service():
    """Authenticate and return Gmail service."""
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                print(f"ERROR: credentials.json not found at {CREDENTIALS_FILE}")
                print("Get it from Google Cloud Console → APIs & Services → Credentials → OAuth 2.0")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
        print(f"✅ Token saved to {TOKEN_FILE}")

    return build("gmail", "v1", credentials=creds)


# ─── Email Helpers ───────────────────────────────────────────────────────────
def decode_body(payload: dict) -> str:
    """Recursively decode email body."""
    body = ""
    if "parts" in payload:
        for part in payload["parts"]:
            body += decode_body(part)
    elif payload.get("mimeType") == "text/plain":
        data = payload.get("body", {}).get("data", "")
        if data:
            body = base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
    return body


def get_header(headers: list, name: str) -> str:
    return next((h["value"] for h in headers if h["name"].lower() == name.lower()), "")


def short_id(email_id: str) -> str:
    """Return last 4 chars as short ID for display."""
    return email_id[-4:].upper()


# ─── Actions ─────────────────────────────────────────────────────────────────
def list_emails(service, limit: int = 10) -> dict:
    """List unread emails."""
    try:
        result = service.users().messages().list(
            userId="me",
            labelIds=["UNREAD", "INBOX"],
            maxResults=limit
        ).execute()

        messages = result.get("messages", [])
        if not messages:
            return {"status": "ok", "count": 0, "emails": [], "message": "No unread emails 🎉"}

        emails = []
        for msg in messages:
            msg_data = service.users().messages().get(userId="me", id=msg["id"], format="metadata").execute()
            headers = msg_data.get("payload", {}).get("headers", [])

            emails.append({
                "id": msg["id"],
                "short_id": short_id(msg["id"]),
                "from": get_header(headers, "From"),
                "subject": get_header(headers, "Subject"),
                "date": get_header(headers, "Date"),
                "snippet": msg_data.get("snippet", "")[:120]
            })

        return {"status": "ok", "count": len(emails), "emails": emails}

    except HttpError as e:
        return {"status": "error", "error": str(e)}


def read_email(service, email_id: str) -> dict:
    """Read full email content."""
    # Support short IDs — find matching full ID
    if len(email_id) <= 6:
        result = service.users().messages().list(userId="me", maxResults=50).execute()
        messages = result.get("messages", [])
        match = next((m["id"] for m in messages if m["id"].endswith(email_id.lower())), None)
        if not match:
            return {"status": "error", "error": f"No email found with ID ending in {email_id}"}
        email_id = match

    try:
        msg = service.users().messages().get(userId="me", id=email_id, format="full").execute()
        headers = msg["payload"]["headers"]
        body = decode_body(msg["payload"])

        # Mark as read
        service.users().messages().modify(
            userId="me", id=email_id,
            body={"removeLabelIds": ["UNREAD"]}
        ).execute()

        return {
            "status": "ok",
            "id": email_id,
            "from": get_header(headers, "From"),
            "to": get_header(headers, "To"),
            "subject": get_header(headers, "Subject"),
            "date": get_header(headers, "Date"),
            "body": body[:3000]  # Truncate for AI consumption
        }

    except HttpError as e:
        return {"status": "error", "error": str(e)}


def reply_to_email(service, email_id: str, body_text: str) -> dict:
    """Reply to an email."""
    original = read_email(service, email_id)
    if original.get("status") == "error":
        return original

    # Resolve full ID if needed
    if len(email_id) <= 6:
        email_id = original["id"]

    msg = service.users().messages().get(userId="me", id=email_id, format="full").execute()
    thread_id = msg["threadId"]
    headers = msg["payload"]["headers"]

    reply_to = get_header(headers, "Reply-To") or get_header(headers, "From")
    subject = get_header(headers, "Subject")
    message_id_header = get_header(headers, "Message-ID")

    if not subject.startswith("Re:"):
        subject = "Re: " + subject

    mime_msg = MIMEMultipart()
    mime_msg["To"] = reply_to
    mime_msg["Subject"] = subject
    mime_msg["In-Reply-To"] = message_id_header
    mime_msg["References"] = message_id_header
    mime_msg.attach(MIMEText(body_text, "plain"))

    raw = base64.urlsafe_b64encode(mime_msg.as_bytes()).decode()

    try:
        sent = service.users().messages().send(
            userId="me",
            body={"raw": raw, "threadId": thread_id}
        ).execute()
        return {"status": "ok", "message": f"Reply sent to {reply_to}", "message_id": sent["id"]}
    except HttpError as e:
        return {"status": "error", "error": str(e)}


def send_email(service, to: str, subject: str, body_text: str) -> dict:
    """Send a new email."""
    mime_msg = MIMEMultipart()
    mime_msg["To"] = to
    mime_msg["Subject"] = subject
    mime_msg.attach(MIMEText(body_text, "plain"))

    raw = base64.urlsafe_b64encode(mime_msg.as_bytes()).decode()

    try:
        sent = service.users().messages().send(
            userId="me",
            body={"raw": raw}
        ).execute()
        return {"status": "ok", "message": f"Email sent to {to}", "message_id": sent["id"]}
    except HttpError as e:
        return {"status": "error", "error": str(e)}


# ─── Entry Point ─────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Gmail Email Manager")
    parser.add_argument("--auth", action="store_true", help="Authenticate with Gmail (first time)")
    parser.add_argument("--action", choices=["list", "read", "reply", "send"], help="Action to perform")
    parser.add_argument("--limit", type=int, default=10, help="Number of emails to list")
    parser.add_argument("--id", type=str, help="Email ID (for read/reply)")
    parser.add_argument("--to", type=str, help="Recipient email (for send)")
    parser.add_argument("--subject", type=str, help="Email subject (for send)")
    parser.add_argument("--body", type=str, help="Email body (for reply/send)")
    args = parser.parse_args()

    service = get_gmail_service()

    if args.auth:
        print("✅ Gmail authentication successful!")
        return

    if args.action == "list":
        result = list_emails(service, args.limit)
    elif args.action == "read":
        if not args.id:
            print("ERROR: --id required for read action")
            sys.exit(1)
        result = read_email(service, args.id)
    elif args.action == "reply":
        if not args.id or not args.body:
            print("ERROR: --id and --body required for reply action")
            sys.exit(1)
        result = reply_to_email(service, args.id, args.body)
    elif args.action == "send":
        if not args.to or not args.subject or not args.body:
            print("ERROR: --to, --subject, and --body required for send action")
            sys.exit(1)
        result = send_email(service, args.to, args.subject, args.body)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
