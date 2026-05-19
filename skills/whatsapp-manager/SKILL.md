---
name: whatsapp_manager
description: Handles WhatsApp inbound messages and replies using the DeepSeek model.
metadata:
  openclaw:
    requires:
      bins: ["python"]
      config: ["setup/config/openclaw.json"]
---

# WhatsApp Manager Skill

This skill is focused on WhatsApp automation using OpenClaw and the DeepSeek model.

## Purpose
- Receive WhatsApp messages from your phone number only
- Understand, summarize, and draft professional replies
- Keep the first stage text-only, using DeepSeek as the brain
- Add voice support later with OpenAI if desired

## Setup
1. Add your DeepSeek API key to `C:\Users\USER\.openclaw\.env`:
   ```powershell
   DEEPSEEK_API_KEY=sk-<your-key>
   WHATSAPP_NUMBER=+923036039298
   ```
2. Confirm OpenClaw has a valid config:
   ```powershell
   openclaw config validate
   ```
3. Start the daemon and dashboard:
   ```powershell
   openclaw onboard --install-daemon
   openclaw dashboard
   ```
4. Scan the WhatsApp QR code from the dashboard in your WhatsApp app.

## WhatsApp prompt flow

### 1. Summarize an incoming message
Use this when you want a quick understanding of the sender's intent.

```bash
exec: python ~/.openclaw/skills/whatsapp-manager/scripts/whatsapp_prompt_flow.py --action summarize --message "<incoming message text>"
```

### 2. Draft a professional reply
Use this when you need a polished response to the sender.

```bash
exec: python ~/.openclaw/skills/whatsapp-manager/scripts/whatsapp_prompt_flow.py --action draft --message "<incoming message text>"
```

### 3. Full reply workflow
Use this when you want both summary and reply in one step.

```bash
exec: python ~/.openclaw/skills/whatsapp-manager/scripts/whatsapp_prompt_flow.py --action workflow --message "<incoming message text>"
```

## Recommended WhatsApp commands

Send these exact phrases to your connected WhatsApp number:

- "Summarize my last message."
- "Draft a short professional reply to this message."
- "Help me respond to this recruiter politely."
- "Write a concise answer and ask for the next step."
- "Explain this message in one sentence."

See [COMMANDS.md](COMMANDS.md) for the full command mapping and trigger phrases.

## Quick-Action Templates

For common scenarios like job inquiries, recruiter messages, and network requests, use pre-built prompt templates:

- **Job Inquiry Response** — Recruiter asking about availability
- **Acknowledgment Reply** — Thanks and appreciation messages
- **Question Response** — Information requests
- **Schedule/Meeting Response** — Meeting requests and availability
- **Project Collaboration Offer** — Work and partnership proposals
- **Networking/Cold Outreach** — New connections and introductions
- **Salary/Negotiation** — Rate and compensation discussions
- **Feedback / Code Review** — Review and mentoring requests
- **Urgent Request** — Time-sensitive help requests
- **Professional Decline** — Turning down opportunities politely

See [QUICK_ACTIONS.md](QUICK_ACTIONS.md) for templates and examples for each scenario.

## How to use quick actions in OpenClaw

1. Identify which template matches the incoming message
2. Tell the assistant: `"Use the [template name] for this message"`
3. Include the incoming message text
4. OpenClaw applies the template and generates a professional reply

### Example

**Incoming message (from recruiter):**
> "Hi Islahuddin, are you interested in a React Developer role at Acme Corp, $50k/month?"

**You send to WhatsApp:**
> "Use the job inquiry template for this recruiter message"

**Assistant responds:**
> "Thank you for the opportunity! I'm very interested in React development roles. Could you share the full job description, tech stack, and timeline? I believe my MERN experience would be a great fit for your team."

## Notes
- This skill does not require OpenAI for text replies.
- If you later want voice notes, add `OPENAI_API_KEY` to your `.env`.
- Keep `WHATSAPP_NUMBER` consistent between `~/.openclaw\.env` and `setup/config/openclaw.json`.

## Next phase
Once WhatsApp is stable, move on to:
- Email automation via the `email_manager` skill
- Job search/apply via the `job_hunt` and `linkedin_apply` skills
- Higher-level workflows after the base chat path is stable
