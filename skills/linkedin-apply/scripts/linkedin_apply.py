#!/usr/bin/env python3
"""
LinkedIn Job Apply Automation Script
Searches LinkedIn jobs and applies to Easy Apply positions.

Usage:
  python linkedin_apply.py --search "react developer" --location "Remote" --limit 10
  python linkedin_apply.py --search "full stack" --apply --limit 5
  python linkedin_apply.py --url "https://linkedin.com/jobs/view/..." --apply
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
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent
SESSION_FILE = Path.home() / ".openclaw" / "linkedin_session.json"
RESUME_FILE = PROJECT_ROOT / "data" / "resume.json"
LOG_FILE = PROJECT_ROOT / "data" / "applications_log.json"

LINKEDIN_JOBS_URL = "https://www.linkedin.com/jobs/search/"


# ─── Helpers ────────────────────────────────────────────────────────────────
def human_delay(min_ms=800, max_ms=2000):
    time.sleep(random.uniform(min_ms / 1000, max_ms / 1000))


def load_resume() -> dict:
    if not RESUME_FILE.exists():
        print(f"ERROR: Resume not found at {RESUME_FILE}. Fill in data/resume.json first.")
        sys.exit(1)
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


def is_already_applied(job_url: str, log: list) -> bool:
    return any(entry.get("job_url") == job_url for entry in log)


def add_to_log(log: list, job: dict, status: str, error: str | None = None):
    log.append({
        "timestamp": datetime.now().isoformat(),
        "platform": "linkedin",
        "job_title": job.get("title", "Unknown"),
        "company": job.get("company", "Unknown"),
        "job_url": job.get("url", ""),
        "status": status,
        "error": error
    })


# ─── Job Search ──────────────────────────────────────────────────────────────
def search_jobs(page, query: str, location: str = "Remote", limit: int = 10) -> list:
    """Search LinkedIn jobs and return a list of job objects."""
    params = f"?keywords={query.replace(' ', '%20')}&location={location.replace(' ', '%20')}&f_WT=2&f_AL=true"
    url = LINKEDIN_JOBS_URL + params

    print(f"Searching: {url}")
    page.goto(url, wait_until="domcontentloaded")
    human_delay(2000, 3000)

    jobs = []
    job_cards = page.locator(".jobs-search__results-list li, .job-card-container")
    count = min(job_cards.count(), limit)

    print(f"Found {job_cards.count()} results, processing {count}...")

    for i in range(count):
        try:
            card = job_cards.nth(i)
            card.click()
            human_delay(1500, 2500)

            # Extract job details from the side panel
            title = page.locator(".job-details-jobs-unified-top-card__job-title, h1.t-24").first.text_content() or "Unknown"
            company = page.locator(".job-details-jobs-unified-top-card__company-name, .job-details-jobs-unified-top-card__primary-description a").first.text_content() or "Unknown"
            job_url = page.url

            # Check for Easy Apply badge
            easy_apply = page.locator(".jobs-apply-button--top-card, button[aria-label*='Easy Apply']").count() > 0

            # Salary (if shown)
            salary_el = page.locator(".compensation__salary, .job-details-preferences-and-skills__item:has([data-tracking-control-name='salary'])").first
            salary = salary_el.text_content().strip() if salary_el.count() > 0 else None

            jobs.append({
                "title": title.strip(),
                "company": company.strip(),
                "url": job_url,
                "salary": salary,
                "easy_apply": easy_apply,
                "index": i + 1
            })
        except Exception as e:
            print(f"  Warning: Could not parse job card {i+1}: {e}")
            continue

    return jobs


# ─── Easy Apply ──────────────────────────────────────────────────────────────
def apply_easy_apply(page, job: dict, resume: dict) -> dict:
    """Fill and submit an Easy Apply form."""
    page.goto(job["url"], wait_until="domcontentloaded")
    human_delay(2000, 3000)

    # Click Easy Apply button
    apply_btn = page.locator("button[aria-label*='Easy Apply'], .jobs-apply-button--top-card")
    if apply_btn.count() == 0:
        return {"success": False, "reason": "No Easy Apply button found"}

    apply_btn.first.click()
    human_delay(2000, 3000)

    step = 1
    max_steps = 10

    while step <= max_steps:
        # Check if there's a Submit button (final step)
        submit_btn = page.locator("button[aria-label*='Submit application'], button:has-text('Submit application')")
        if submit_btn.count() > 0:
            submit_btn.first.click()
            human_delay(2000, 3000)
            print(f"  ✅ Submitted!")
            return {"success": True}

        # Check for Next/Continue button
        next_btn = page.locator("button[aria-label*='Continue to next step'], button:has-text('Next'), button:has-text('Continue')")

        # Auto-fill visible input fields
        inputs = page.locator("input[type='text']:visible, input[type='tel']:visible, input[type='email']:visible, textarea:visible")
        for inp in inputs.element_handles():
            try:
                label_id = inp.get_attribute("id")
                aria_label = inp.get_attribute("aria-label") or ""
                label_text = (aria_label + " " + (page.locator(f'label[for="{label_id}"]').text_content() or "")).lower()

                current_val = inp.evaluate("el => el.value")
                if current_val:
                    continue  # Already filled

                # Map fields to resume data
                fill_value = None
                personal = resume["personal"]
                professional = resume["professional"]

                if "first name" in label_text or "firstname" in label_text:
                    fill_value = personal["firstName"]
                elif "last name" in label_text or "lastname" in label_text:
                    fill_value = personal["lastName"]
                elif "email" in label_text:
                    fill_value = personal["email"]
                elif "phone" in label_text or "mobile" in label_text:
                    fill_value = personal["phone"]
                elif "linkedin" in label_text:
                    fill_value = personal["linkedin"]
                elif "website" in label_text or "portfolio" in label_text:
                    fill_value = personal["portfolio"]
                elif "city" in label_text or "location" in label_text:
                    fill_value = personal["location"]["city"]
                elif "experience" in label_text or "years" in label_text:
                    fill_value = str(professional["yearsExperience"])
                elif "salary" in label_text or "compensation" in label_text:
                    fill_value = str(professional["salaryExpectation"]["min"])
                elif "github" in label_text:
                    fill_value = personal["github"]

                if fill_value:
                    inp.fill(fill_value)
                    human_delay(200, 500)

            except Exception:
                continue

        # Click Next if available
        if next_btn.count() > 0:
            next_btn.first.click()
            human_delay(1500, 2500)
            step += 1
        else:
            # No next, no submit — might be stuck or done
            break

    return {"success": False, "reason": "Could not find submit button after all steps"}


# ─── Main Search/Apply Flow ───────────────────────────────────────────────────
def run(query: str, location: str, limit: int, do_apply: bool, job_url: str | None):
    if not SESSION_FILE.exists():
        print("ERROR: No LinkedIn session. Run linkedin_post.py --login first.")
        sys.exit(1)

    resume = load_resume()
    log = load_log()
    results = {"jobs": [], "applied": [], "skipped": [], "failed": []}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=str(SESSION_FILE))
        page = context.new_page()

        # Single URL mode
        if job_url:
            jobs_to_process = [{"title": "Unknown", "company": "Unknown", "url": job_url, "easy_apply": True}]
        else:
            jobs_to_process = search_jobs(page, query, location, limit)

        results["jobs"] = jobs_to_process

        if do_apply:
            for job in jobs_to_process:
                if is_already_applied(job["url"], log):
                    print(f"  ⏭️  Already applied: {job['title']} @ {job['company']}")
                    results["skipped"].append(job)
                    continue

                if not job.get("easy_apply", False):
                    print(f"  ⏭️  Not Easy Apply: {job['title']} @ {job['company']}")
                    results["skipped"].append(job)
                    continue

                print(f"  Applying: {job['title']} @ {job['company']}...")
                apply_result = apply_easy_apply(page, job, resume)

                if apply_result.get("success"):
                    add_to_log(log, job, "applied")
                    results["applied"].append(job)
                else:
                    add_to_log(log, job, "failed", apply_result.get("reason"))
                    results["failed"].append(job)
                    print(f"  ❌ Failed: {apply_result.get('reason')}")

                human_delay(3000, 6000)  # Polite delay between applications

            save_log(log)

        browser.close()

    # Print summary
    print(json.dumps(results, indent=2))
    return results


# ─── Entry Point ─────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="LinkedIn Job Apply Automation")
    parser.add_argument("--search", type=str, help="Job search keywords")
    parser.add_argument("--location", type=str, default="Remote", help="Job location")
    parser.add_argument("--limit", type=int, default=10, help="Max jobs to process")
    parser.add_argument("--apply", action="store_true", help="Auto-apply to Easy Apply jobs")
    parser.add_argument("--url", type=str, help="Apply to a specific LinkedIn job URL")
    args = parser.parse_args()

    if not args.search and not args.url:
        parser.print_help()
        sys.exit(1)

    run(
        query=args.search or "",
        location=args.location,
        limit=args.limit,
        do_apply=args.apply,
        job_url=args.url
    )


if __name__ == "__main__":
    main()
