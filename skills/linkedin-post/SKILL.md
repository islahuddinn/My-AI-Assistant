---
name: linkedin_post
description: Posts text, images, or articles to LinkedIn on behalf of the user.
metadata:
  openclaw:
    requires:
      bins: ["python"]
---

# LinkedIn Post Skill

You can post content to LinkedIn on behalf of the user.

## When to use this skill
When the user says something like:
- "post to linkedin: ..."
- "share on linkedin: ..."
- "create a linkedin post about ..."
- "publish to linkedin: ..."

## How to use this skill

1. **Confirm first** — Always repeat back the exact post content and ask for confirmation before posting. Only skip confirmation if the user explicitly says "go ahead" or "post it now".

2. **Execute** — Run the post script:
```
exec: python ~/.openclaw/skills/linkedin-post/scripts/linkedin_post.py --content "<exact_content>"
```

3. **With image** — If the user provides an image path or URL:
```
exec: python ~/.openclaw/skills/linkedin-post/scripts/linkedin_post.py --content "<content>" --image "<image_path>"
```

## Output format
After execution, report:
- ✅ Whether the post was successful
- 🔗 The URL of the published post if captured
- ❌ Any error message if it failed

## Notes
- The script opens a Playwright browser session using the user's saved LinkedIn cookies. The user must have logged into LinkedIn once via the script's `--login` flag.
- Do not modify the content — post it verbatim as provided by the user.
- Hashtags, line breaks, and emojis are all supported.
