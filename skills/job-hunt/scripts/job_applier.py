#!/usr/bin/env python3
"""
Remote Job Applier — Opens application URLs and auto-fills forms using Playwright.

Usage:
  python job_applier.py --query "react developer" --limit 5
  python job_applier.py --url "https://remoteok.com/jobs/12345"
"""

import argparse
import json
import subprocess
import sys
import time
import random
from datetime import datetime
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("ERROR: Playwright not installed. Run: pip install playwright && playwright install chromium")
    sys.exit(1)

# ─── Config ─────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent
RESUME_FILE = PROJECT_ROOT / "data" / "resume.json"
LOG_FILE = PROJECT_ROOT / "data" / "applications_log.json"
SESSION_FILE = Path.home() / ".openclaw" / "linkedin_session.json"


# ─── Helpers ─────────────────────────────────────────────────────────────────
def human_delay(min_ms=600, max_ms=1800):
    time.sleep(random.uniform(min_ms / 1000, max_ms / 1000))


def load_resume() -> dict:
    with open(RESUME_FILE) as f:
        return json.load(f)


def load_log() -> list:
    if LOG_FILE.exists():
        with open(LOG_FILE) as f:
            return json.load(f)
    return []


def save_log(log: list):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)


def is_already_applied(url: str, log: list) -> bool:
    return any(entry.get("job_url") == url for entry in log)


def add_to_log(log: list, job: dict, status: str, error: str | None = None):
    log.append({
        "timestamp": datetime.now().isoformat(),
        "platform": job.get("source", "unknown"),
        "job_title": job.get("title", "Unknown"),
        "company": job.get("company", "Unknown"),
        "job_url": job.get("url", ""),
        "status": status,
        "error": error
    })


# ─── Smart Form Filler ────────────────────────────────────────────────────────
def fill_form_fields(page, resume: dict):
    """Try to intelligently fill form fields using resume data."""
    personal = resume["personal"]
    professional = resume["professional"]
    links = resume.get("links", {})

    # Field mapping: keywords → value
    field_map = {
        "first name": personal["firstName"],
        "firstname": personal["firstName"],
        "last name": personal["lastName"],
        "lastname": personal["lastName"],
        "full name": f"{personal['firstName']} {personal['lastName']}",
        "name": f"{personal['firstName']} {personal['lastName']}",
        "email": personal["email"],
        "e-mail": personal["email"],
        "phone": personal["phone"],
        "mobile": personal["phone"],
        "telephone": personal["phone"],
        "linkedin": personal["linkedin"],
        "github": personal["github"],
        "portfolio": personal["portfolio"],
        "website": personal["portfolio"],
        "city": personal["location"]["city"],
        "location": personal["location"]["city"],
        "country": personal["location"]["country"],
        "years of experience": str(professional["yearsExperience"]),
        "years experience": str(professional["yearsExperience"]),
        "salary": str(professional["salaryExpectation"]["min"]),
        "expected salary": str(professional["salaryExpectation"]["min"]),
        "cover letter": links.get("coverLetterTemplate", ""),
        "resume url": links.get("resumePDF", ""),
    }

    try:
        inputs = page.locator("input:visible, textarea:visible")
        for i in range(inputs.count()):
            try:
                inp = inputs.nth(i)
                inp_type = inp.get_attribute("type") or "text"

                if inp_type in ("submit", "button", "hidden", "checkbox", "radio", "file"):
                    continue

                current = inp.evaluate("el => el.value")
                if current and current.strip():
                    continue  # Already filled

                # Get label context
                input_id = inp.get_attribute("id") or ""
                placeholder = (inp.get_attribute("placeholder") or "").lower()
                aria_label = (inp.get_attribute("aria-label") or "").lower()
                name_attr = (inp.get_attribute("name") or "").lower()

                label_text = ""
                if input_id:
                    label_el = page.locator(f'label[for="{input_id}"]')
                    if label_el.count() > 0:
                        label_text = (label_el.first.text_content() or "").lower()

                searchable = f"{label_text} {placeholder} {aria_label} {name_attr}"

                fill_value = None
                for keyword, value in field_map.items():
                    if keyword in searchable:
                        fill_value = value
                        break

                if fill_value:
                    inp.fill(fill_value)
                    human_delay(100, 300)

            except Exception:
                continue

    except Exception as e:
        print(f"  Warning: Form fill error: {e}")


# ─── Generic Apply ────────────────────────────────────────────────────────────
def apply_to_url(page, job: dict, resume: dict) -> dict:
    """Navigate to a job URL and attempt to apply."""
    url = job["url"]
    print(f"  Opening: {url}")

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        human_delay(2000, 3500)

        # Look for an "Apply" button
        apply_btn = page.locator(
            "a:has-text('Apply'), button:has-text('Apply'), "
            "a:has-text('Apply Now'), button:has-text('Apply Now'), "
            "[class*='apply-btn'], [data-apply], a[href*='apply']"
        ).first

        if apply_btn.count() == 0:
            # Maybe this IS the application form
            form = page.locator("form").first
            if form.count() > 0:
                fill_form_fields(page, resume)
                submit = page.locator("button[type='submit'], input[type='submit']").first
                if submit.count() > 0:
                    human_delay(1000, 2000)
                    submit.click()
                    human_delay(2000, 3000)
                    return {"success": True, "method": "direct_form"}
            return {"success": False, "reason": "No apply button or form found"}

        # Click apply button
        with page.expect_navigation(wait_until="domcontentloaded", timeout=15000):
            apply_btn.click()

        human_delay(2000, 3000)

        # Fill the application form
        fill_form_fields(page, resume)
        human_delay(1000, 2000)

        # Submit
        submit = page.locator("button[type='submit'], input[type='submit'], button:has-text('Submit')").first
        if submit.count() > 0:
            submit.click()
            human_delay(2000, 4000)

            # Check for success indicators
            success_text = page.locator(
                ":has-text('Thank you'), :has-text('Application received'), "
                ":has-text('Successfully applied'), :has-text('application submitted')"
            ).count()

            if success_text > 0:
                return {"success": True, "method": "form_submit"}
            else:
                # Ambiguous — might have succeeded
                return {"success": True, "method": "form_submit_unverified"}
        else:
            return {"success": False, "reason": "Could not find submit button"}

    except PlaywrightTimeout:
        return {"success": False, "reason": "Timeout loading page"}
    except Exception as e:
        return {"success": False, "reason": str(e)}


# ─── Main ────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Remote Job Auto-Applier")
    parser.add_argument("--query", type=str, help="Search keywords (searches all boards first)")
    parser.add_argument("--url", type=str, help="Apply to a specific job URL")
    parser.add_argument("--limit", type=int, default=5, help="Max applications to attempt")
    args = parser.parse_args()

    resume = load_resume()
    log = load_log()
    results = {"applied": [], "skipped": [], "failed": []}

    # Build job list
    jobs = []
    if args.url:
        jobs = [{"title": "Unknown", "company": "Unknown", "url": args.url, "source": "direct"}]
    elif args.query:
        # Run the scraper script to get jobs
        scraper = SCRIPT_DIR / "job_scraper.py"
        proc = subprocess.run(
            [sys.executable, str(scraper), "--query", args.query, "--limit", str(args.limit * 3)],
            capture_output=True, text=True
        )
        try:
            # Parse just the JSON part from output
            output = proc.stdout
            json_start = output.rfind("{")
            if json_start >= 0:
                scraper_result = json.loads(output[json_start:])
                jobs = scraper_result.get("jobs", [])
        except Exception as e:
            print(f"ERROR: Could not parse scraper output: {e}")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

    # Filter out already applied
    new_jobs = [j for j in jobs if not is_already_applied(j["url"], log)]
    jobs_to_apply = new_jobs[:args.limit]

    print(f"\n📋 {len(jobs_to_apply)} new jobs to apply to (skipping {len(jobs) - len(new_jobs)} already applied)\n")

    if not jobs_to_apply:
        print("No new jobs to apply to.")
        print(json.dumps(results))
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            storage_state=str(SESSION_FILE) if SESSION_FILE.exists() else None,
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()

        for job in jobs_to_apply:
            print(f"\n→ {job['title']} @ {job['company']} [{job.get('source', '?')}]")
            result = apply_to_url(page, job, resume)

            if result.get("success"):
                print(f"  ✅ Applied! (method: {result.get('method')})")
                add_to_log(log, job, "applied")
                results["applied"].append({"job": job, "method": result.get("method")})
            else:
                print(f"  ❌ Failed: {result.get('reason')}")
                add_to_log(log, job, "failed", result.get("reason"))
                results["failed"].append({"job": job, "reason": result.get("reason")})

            human_delay(4000, 8000)  # Polite delay between applications

        browser.close()

    save_log(log)

    summary = {
        "total_attempted": len(jobs_to_apply),
        "applied": len(results["applied"]),
        "failed": len(results["failed"]),
        "details": results
    }

    print("\n" + "=" * 50)
    print(f"✅ Applied: {summary['applied']} | ❌ Failed: {summary['failed']}")
    print("=" * 50)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
