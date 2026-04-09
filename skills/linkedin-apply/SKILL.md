---
name: linkedin_apply
description: Searches LinkedIn for remote developer jobs and applies to Easy Apply positions ONLY. Uses Islahuddin's real resume profile (MERN, Node.js, React, Django, Docker). Never applies to external-redirect jobs.
metadata:
  openclaw:
    requires:
      bins: ["python"]
      config: ["data/resume.json"]
---

# LinkedIn Job Apply Skill

You can search for jobs on LinkedIn and apply to Easy Apply positions automatically.

## When to use this skill
When the user says:
- "find linkedin jobs: [keywords]"
- "apply linkedin jobs: [role]"
- "search linkedin for [job title] jobs"
- "apply to [X] developer jobs on linkedin"
- "apply to linkedin job: [URL]"

## How to use this skill

### Search only (no apply):
```
exec: python ~/.openclaw/skills/linkedin-apply/scripts/linkedin_apply.py --search "<keywords>" --location "Remote" --limit 10
```

### Search + Apply (Easy Apply only):
```
exec: python ~/.openclaw/skills/linkedin-apply/scripts/linkedin_apply.py --search "<keywords>" --location "Remote" --apply --limit 5
```

### Apply to a specific job URL:
```
exec: python ~/.openclaw/skills/linkedin-apply/scripts/linkedin_apply.py --url "<linkedin_job_url>" --apply
```

## Workflow
1. **For "find" commands** — search and return a formatted list of jobs (title, company, location, salary, URL). Ask if user wants to apply to any.
2. **For "apply" commands** — confirm with user how many to apply to, then execute. Report results.
3. **Always log** — the script automatically logs to `data/applications_log.json`.

## Output format
Report for each application:
- 📋 Job title + company
- ✅ Applied / ❌ Failed / ⏭️ Skipped (not Easy Apply)
- 🔗 Job URL

Show a summary at the end: "Applied to X out of Y jobs"

## Important rules
- Only apply to **Easy Apply** jobs unless user explicitly says to try external sites too
- Never apply to the same job twice (script checks the log)
- Maximum 10 applications per session unless user specifies more
