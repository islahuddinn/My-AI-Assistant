---
name: job_hunt
description: Searches for remote developer jobs across RemoteOK, Remotive, We Work Remotely, and Byte.com. Can auto-apply to matching positions.
metadata:
  openclaw:
    requires:
      bins: ["python"]
      config: ["data/resume.json"]
---

# Job Hunt Skill

You aggregate remote developer jobs from multiple platforms and can automatically apply.

## Supported platforms
- **RemoteOK** — Public API, instant results
- **Remotive** — Public API, developer-focused
- **We Work Remotely** — RSS feed, high-quality remote jobs
- **Byte.com** — Browser automation (Playwright)

## When to use this skill
- "find remote jobs: [keywords]"
- "search for [role] jobs"
- "any new react developer jobs today?"
- "find fullstack jobs on remoteok"
- "job digest" — same as daily digest
- "apply to remote jobs: [keywords]"

## Commands

### Search all platforms:
```
exec: python ~/.openclaw/skills/job-hunt/scripts/job_scraper.py --query "<keywords>" --limit 10
```

### Search a specific platform:
```
exec: python ~/.openclaw/skills/job-hunt/scripts/job_scraper.py --query "<keywords>" --source remoteok --limit 5
exec: python ~/.openclaw/skills/job-hunt/scripts/job_scraper.py --query "<keywords>" --source remotive --limit 5
exec: python ~/.openclaw/skills/job-hunt/scripts/job_scraper.py --query "<keywords>" --source weworkremotely --limit 5
exec: python ~/.openclaw/skills/job-hunt/scripts/job_scraper.py --query "<keywords>" --source byte --limit 5
```

### Search + Apply:
```
exec: python ~/.openclaw/skills/job-hunt/scripts/job_applier.py --query "<keywords>" --limit 5
```

## Workflow
1. **Search** → return formatted table of jobs
2. **Filter** → exclude any jobs that match user's `preferences.excludeKeywords` in resume.json
3. **Deduplicate** → skip jobs already in `data/applications_log.json`
4. **If apply** → confirm count with user, then execute applier script

## Output format
```
🌐 Remote Jobs Found (12 total)

1. [RemoteOK] Senior React Developer — Acme Corp
   💰 $4,000–$6,000/mo | 🌍 Worldwide | ⏰ 2h ago
   🔗 https://remoteok.com/jobs/123

2. [Remotive] Full Stack Engineer — StartupXYZ
   💰 $5,000/mo | 🌍 Remote | ⏰ 1d ago
   🔗 https://remotive.com/job/456
```

## Daily Digest (automated)
Run by cron job daily at 9 AM. Finds jobs from the past 24 hours matching the user's preferred roles and sends a summary to WhatsApp.

## Important rules
- Never apply to a job already in the applications log
- Maximum 10 applications per run
- Flag salary info when available
- Always include the apply URL
