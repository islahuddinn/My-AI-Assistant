#!/usr/bin/env python3
"""
LinkedIn Post Automation Script
Uses Playwright to post content to LinkedIn in your browser session.

Usage:
  python linkedin_post.py --login                        # First-time login (saves session)
  python linkedin_post.py --content "Your post text"     # Post text
  python linkedin_post.py --content "Text" --image /path/to/image.jpg
"""

import argparse
import json
import sys
import time
import random
from pathlib import Path
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("ERROR: Playwright not installed. Run: pip install playwright && playwright install chromium")
    sys.exit(1)

# ─── Config ─────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent  # d:\Sallu\Ai-Assistant
SESSION_FILE = Path.home() / ".openclaw" / "linkedin_session.json"
LOG_FILE = PROJECT_ROOT / "data" / "linkedin_posts_log.json"

LINKEDIN_URL = "https://www.linkedin.com"
FEED_URL = "https://www.linkedin.com/feed/"


# ─── Helpers ────────────────────────────────────────────────────────────────
def human_delay(min_ms=500, max_ms=1500):
    """Simulate human-like typing/clicking delays."""
    time.sleep(random.uniform(min_ms / 1000, max_ms / 1000))


def human_type(element, text: str):
    """Type text character by character with human-like delays."""
    for char in text:
        element.type(char)
        time.sleep(random.uniform(0.03, 0.12))


def log_post(content: str, image: str | None, success: bool, url: str | None, error: str | None):
    """Append post result to the log file."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    log = []
    if LOG_FILE.exists():
        with open(LOG_FILE) as f:
            log = json.load(f)

    log.append({
        "timestamp": datetime.now().isoformat(),
        "content_preview": content[:100] + ("..." if len(content) > 100 else ""),
        "has_image": image is not None,
        "success": success,
        "post_url": url,
        "error": error
    })

    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)


# ─── Login / Session ─────────────────────────────────────────────────────────
def login_and_save_session():
    """Open a visible browser for the user to log in, then save the session."""
    print("Opening browser for LinkedIn login...")
    print("Please log in manually. The session will be saved automatically.")
    print("Press ENTER here after you have fully logged in.")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(LINKEDIN_URL)

        input("\n>>> Press ENTER after logging in to LinkedIn... ")

        # Save session state
        SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
        context.storage_state(path=str(SESSION_FILE))
        print(f"✅ Session saved to {SESSION_FILE}")
        browser.close()


# ─── Post ────────────────────────────────────────────────────────────────────
def post_to_linkedin(content: str, image_path: str | None = None):
    """Post content to LinkedIn using saved session."""
    if not SESSION_FILE.exists():
        print("ERROR: No LinkedIn session found. Run with --login first.")
        sys.exit(1)

    print(f"Posting to LinkedIn... ({len(content)} characters)")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=str(SESSION_FILE))
        page = context.new_page()

        try:
            # Navigate to feed
            page.goto(FEED_URL, wait_until="domcontentloaded")
            human_delay(2000, 3000)

            # Check if logged in
            if "login" in page.url.lower() or "signup" in page.url.lower():
                print("ERROR: Session expired. Run with --login to re-authenticate.")
                log_post(content, image_path, False, None, "Session expired")
                sys.exit(1)

            # Click "Start a post"
            start_post_btn = page.locator('[aria-label*="Start a post"], [data-test-modal-launcher*="post"], button:has-text("Start a post")')
            start_post_btn.first.click()
            human_delay(1500, 2500)

            # Type content in the post editor
            post_editor = page.locator('[role="textbox"][aria-label*="post"], .ql-editor, [data-placeholder*="What do you want to talk about"]')
            post_editor.first.click()
            human_delay(500, 1000)
            human_type(post_editor.first, content)
            human_delay(1000, 2000)

            # Attach image if provided
            if image_path:
                img_path = Path(image_path)
                if not img_path.exists():
                    print(f"WARNING: Image not found: {image_path}. Posting without image.")
                else:
                    photo_btn = page.locator('[aria-label*="Add a photo"], [data-test-icon="image"]')
                    photo_btn.first.click()
                    human_delay(1000, 1500)
                    file_input = page.locator('input[type="file"]')
                    file_input.set_input_files(str(img_path))
                    human_delay(2000, 3000)
                    print(f"  Image attached: {img_path.name}")

            # Click "Post" button
            post_btn = page.locator('button:has-text("Post"), [data-test-button*="post-share"]')
            post_btn.last.click()
            human_delay(3000, 5000)

            # Verify success
            post_url = None
            try:
                # Try to capture the URL or a success indicator
                success_indicator = page.locator('[data-test-share-form-success], .share-box-feed-entry__closed-share-box')
                success_indicator.wait_for(timeout=10000)
                print("✅ Post published successfully!")
            except PlaywrightTimeout:
                # Check if we're back on feed (post usually disappears the modal)
                if "feed" in page.url:
                    print("✅ Post likely published (modal closed).")
                else:
                    raise Exception("Could not confirm post was published.")

            log_post(content, image_path, True, post_url, None)
            return {"success": True, "url": post_url}

        except Exception as e:
            error_msg = str(e)
            print(f"❌ Failed to post: {error_msg}")
            log_post(content, image_path, False, None, error_msg)
            
            # Save screenshot for debugging
            screenshot_path = PROJECT_ROOT / "data" / "debug_linkedin_post.png"
            page.screenshot(path=str(screenshot_path))
            print(f"  Debug screenshot: {screenshot_path}")
            
            return {"success": False, "error": error_msg}

        finally:
            browser.close()


# ─── Main ────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="LinkedIn Post Automation")
    parser.add_argument("--login", action="store_true", help="Log in to LinkedIn and save session")
    parser.add_argument("--content", type=str, help="Post content (text)")
    parser.add_argument("--image", type=str, help="Path to image to attach", default=None)
    args = parser.parse_args()

    if args.login:
        login_and_save_session()
    elif args.content:
        result = post_to_linkedin(args.content, args.image)
        # Output JSON for the AI to parse
        print(json.dumps(result))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
