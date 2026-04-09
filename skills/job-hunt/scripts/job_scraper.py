#!/usr/bin/env python3
"""
Remote Job Scraper — Aggregates jobs from RemoteOK, Remotive, We Work Remotely, and Byte.com

Usage:
  python job_scraper.py --query "react developer" --limit 10
  python job_scraper.py --query "full stack" --source remoteok --limit 5
  python job_scraper.py --query "python" --source remotive
  python job_scraper.py --query "node.js" --source weworkremotely
  python job_scraper.py --query "frontend" --source byte
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

missing = []
try:
    import requests
except ImportError:
    missing.append("requests")
try:
    import feedparser
except ImportError:
    missing.append("feedparser")

if missing:
    print(f"ERROR: Missing packages. Run: pip install {' '.join(missing)}")
    sys.exit(1)

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

# ─── Config ─────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent
RESUME_FILE = PROJECT_ROOT / "data" / "resume.json"
LOG_FILE = PROJECT_ROOT / "data" / "applications_log.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0"
}


# ─── Helpers ─────────────────────────────────────────────────────────────────
def already_applied(url: str) -> bool:
    if LOG_FILE.exists():
        with open(LOG_FILE) as f:
            log = json.load(f)
        return any(entry.get("job_url") == url for entry in log)
    return False


def normalize_job(title: str, company: str, url: str, salary: str | None,
                  tags: list, posted: str | None, source: str) -> dict:
    return {
        "title": title.strip(),
        "company": company.strip(),
        "url": url,
        "salary": salary,
        "tags": tags,
        "posted": posted,
        "source": source,
        "already_applied": already_applied(url)
    }


def filter_jobs(jobs: list, query: str) -> list:
    """Filter jobs by query keywords."""
    keywords = [k.lower() for k in query.split()]
    filtered = []
    for job in jobs:
        searchable = f"{job['title']} {job['company']} {' '.join(job.get('tags', []))}".lower()
        if any(kw in searchable for kw in keywords):
            filtered.append(job)
    return filtered


# ─── RemoteOK ────────────────────────────────────────────────────────────────
def fetch_remoteok(query: str, limit: int) -> list:
    """Fetch from RemoteOK public JSON API."""
    print("  Fetching RemoteOK...")
    try:
        resp = requests.get("https://remoteok.com/remote-jobs.json", headers=HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        # Skip first item (it's metadata)
        jobs_raw = [j for j in data[1:] if isinstance(j, dict)]
        jobs = []

        for j in jobs_raw[:100]:  # Limit initial fetch
            title = j.get("position", "")
            company = j.get("company", "")
            url = j.get("url", f"https://remoteok.com/jobs/{j.get('id', '')}")
            salary = None
            if j.get("salary_min") and j.get("salary_max"):
                salary = f"${j['salary_min']:,}–${j['salary_max']:,}/yr"
            tags = j.get("tags", [])
            posted = j.get("date", None)

            if title and company:
                jobs.append(normalize_job(title, company, url, salary, tags, posted, "remoteok"))

        filtered = filter_jobs(jobs, query)
        return filtered[:limit]

    except Exception as e:
        print(f"  RemoteOK error: {e}")
        return []


# ─── Remotive ────────────────────────────────────────────────────────────────
def fetch_remotive(query: str, limit: int) -> list:
    """Fetch from Remotive public API."""
    print("  Fetching Remotive...")
    try:
        url = f"https://remotive.com/api/remote-jobs?category=software-dev&limit=50&search={query.replace(' ', '+')}"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        jobs = []
        for j in data.get("jobs", []):
            title = j.get("title", "")
            company = j.get("company_name", "")
            job_url = j.get("url", "")
            salary = j.get("salary", None)
            tags = j.get("tags", [])
            posted = j.get("publication_date", None)

            if title and company:
                jobs.append(normalize_job(title, company, job_url, salary, tags, posted, "remotive"))

        return jobs[:limit]

    except Exception as e:
        print(f"  Remotive error: {e}")
        return []


# ─── We Work Remotely ────────────────────────────────────────────────────────
def fetch_weworkremotely(query: str, limit: int) -> list:
    """Fetch from We Work Remotely RSS feed."""
    print("  Fetching We Work Remotely...")
    try:
        feed = feedparser.parse("https://weworkremotely.com/remote-programming-jobs.rss")
        jobs = []

        for entry in feed.entries:
            title = entry.get("title", "")
            company = entry.get("author", "") or title.split(":")[0] if ":" in title else "Unknown"
            job_url = entry.get("link", "")
            posted = entry.get("published", None)
            tags = []

            # Filter by query
            searchable = (title + " " + entry.get("summary", "")).lower()
            keywords = query.lower().split()
            if any(kw in searchable for kw in keywords):
                jobs.append(normalize_job(title, company, job_url, None, tags, posted, "weworkremotely"))

        return jobs[:limit]

    except Exception as e:
        print(f"  We Work Remotely error: {e}")
        return []


# ─── Byte.com ─────────────────────────────────────────────────────────────────
def fetch_byte(query: str, limit: int) -> list:
    """Fetch from Byte.com using Playwright browser automation."""
    if not PLAYWRIGHT_AVAILABLE:
        print("  Byte.com: Playwright not available, skipping.")
        return []

    print("  Fetching Byte.com (browser)...")
    jobs = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            search_url = f"https://byte.com/jobs?search={query.replace(' ', '+')}&remote=true"
            page.goto(search_url, wait_until="domcontentloaded", timeout=20000)
            time.sleep(3)

            # Try to extract job cards
            job_cards = page.locator("[data-testid='job-card'], .job-listing, article.job")
            count = min(job_cards.count(), limit)

            for i in range(count):
                try:
                    card = job_cards.nth(i)
                    title_el = card.locator("h2, h3, .job-title").first
                    company_el = card.locator(".company, .company-name").first
                    link_el = card.locator("a").first

                    title = title_el.text_content().strip() if title_el.count() > 0 else "Unknown"
                    company = company_el.text_content().strip() if company_el.count() > 0 else "Unknown"
                    href = link_el.get_attribute("href") if link_el.count() > 0 else ""
                    if href and not href.startswith("http"):
                        href = "https://byte.com" + href

                    if title and company:
                        jobs.append(normalize_job(title, company, href, None, [], None, "byte"))
                except Exception:
                    continue

            browser.close()

    except Exception as e:
        print(f"  Byte.com error: {e}")

    return jobs


# ─── Main ────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Remote Job Scraper")
    parser.add_argument("--query", type=str, required=True, help="Job search keywords")
    parser.add_argument("--source", choices=["all", "remoteok", "remotive", "weworkremotely", "byte"], default="all")
    parser.add_argument("--limit", type=int, default=10, help="Max jobs per source")
    args = parser.parse_args()

    all_jobs = []
    per_source_limit = args.limit

    print(f"\n🔍 Searching for: '{args.query}' (source: {args.source})\n")

    if args.source in ("all", "remoteok"):
        all_jobs.extend(fetch_remoteok(args.query, per_source_limit))

    if args.source in ("all", "remotive"):
        all_jobs.extend(fetch_remotive(args.query, per_source_limit))

    if args.source in ("all", "weworkremotely"):
        all_jobs.extend(fetch_weworkremotely(args.query, per_source_limit))

    if args.source in ("all", "byte"):
        all_jobs.extend(fetch_byte(args.query, per_source_limit))

    # Deduplicate by URL
    seen_urls = set()
    unique_jobs = []
    for job in all_jobs:
        if job["url"] not in seen_urls:
            seen_urls.add(job["url"])
            unique_jobs.append(job)

    result = {
        "query": args.query,
        "timestamp": datetime.now().isoformat(),
        "total": len(unique_jobs),
        "jobs": unique_jobs
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
