---
name: email_manager
description: Manages Gmail inbox — reads, summarizes, drafts, and sends emails.
metadata:
  openclaw:
    requires:
      bins: ["python"]
      config: ["data/credentials.json"]
---

# Email Manager Skill

You can read, summarize, draft, and send emails from the user's Gmail account.

## When to use this skill
- "check my email" / "what's in my inbox"
- "summarize my unread emails"
- "reply to email from [name]: [content]"
- "send email to [email]: [subject] — [body]"
- "draft email to [name]"
- "any important emails?"
- "mark [email] as read"

## How to use this skill

### Check inbox / summarize unread:
```
exec: python ~/.openclaw/skills/email-manager/scripts/email_manager.py --action list --limit 10
```

### Reply to an email (by ID):
```
exec: python ~/.openclaw/skills/email-manager/scripts/email_manager.py --action reply --id "<email_id>" --body "<reply_text>"
```

### Send a new email:
```
exec: python ~/.openclaw/skills/email-manager/scripts/email_manager.py --action send --to "<email>" --subject "<subject>" --body "<body>"
```

### Read a specific email:
```
exec: python ~/.openclaw/skills/email-manager/scripts/email_manager.py --action read --id "<email_id>"
```

## Workflow
1. **For "check email"** — list unread emails with ID, sender, subject, and a 1-sentence snippet
2. **For replies** — always confirm the reply content before sending
3. **For drafts** — compose and show the draft; ask "Should I send this?"
4. **Format IDs** — show short 4-character IDs in your summary for easy reference

## Output format
```
📧 Email Summary (3 unread)

[A1] From: recruiter@company.com — "Full Stack Developer Role"
     → "Hi, we'd love to discuss..."

[A2] From: client@startup.io — "Project Update"
     → "The latest build looks great..."
```

## Important rules
- Never send an email without explicit confirmation from the user
- When drafting, use the user's professional tone (see system prompt)
- Priority/starred emails should be highlighted
