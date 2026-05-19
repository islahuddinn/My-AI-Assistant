# WhatsApp Manager — Quick Start Guide

Welcome! This folder contains everything you need to automate WhatsApp message replies with OpenClaw and DeepSeek.

---

## 📁 File Structure

| File | Purpose |
|------|---------|
| **SKILL.md** | Main skill documentation — how to use the WhatsApp manager |
| **INSTRUCTIONS.md** | System instructions for OpenClaw AI behavior on WhatsApp |
| **COMMANDS.md** | Command mappings — what phrases trigger what actions |
| **QUICK_ACTIONS.md** | Pre-built prompt templates for 10 common scenarios |
| **scripts/whatsapp_prompt_flow.py** | Python script for summarize, draft, and workflow actions |

---

## 🚀 Quick Start (3 steps)

### 1. Add your DeepSeek API key
```powershell
notepad "$env:USERPROFILE\.openclaw\.env"
```
Set:
```
DEEPSEEK_API_KEY=sk-<your-actual-key>
WHATSAPP_NUMBER=+923036039298
```

### 2. Start OpenClaw
```powershell
openclaw onboard --install-daemon
openclaw dashboard
```

### 3. Scan WhatsApp QR and send a test message
Open the dashboard URL and scan the WhatsApp QR code.

Send to WhatsApp:
> "Summarize my last message" or "Draft a reply to this message"

---

## 📖 How to Use

### For basic tasks:
1. **Summarize a message** → `"Summarize my last message"`
2. **Draft a reply** → `"Draft a professional reply"`
3. **Full workflow** → `"Help me respond to this message"`

See **COMMANDS.md** for all trigger phrases.

### For specific scenarios:
Use a **Quick Action template** based on the message type:
- Job inquiry? → Job Inquiry Response template
- Thanks message? → Acknowledgment Reply template
- Question? → Question Response template
- Meeting request? → Schedule/Meeting Response template

See **QUICK_ACTIONS.md** for all 10 templates with examples.

### For advanced customization:
Edit **INSTRUCTIONS.md** to:
- Add new scenario-based responses
- Modify tone and style guidelines
- Add standing rules or preferences

---

## 🎯 Example Workflows

### Workflow 1: Job Inquiry
```
Incoming: "Hi, are you available for a React developer role?"
You send:  "Use the job inquiry template"
Assistant: "Thank you for the opportunity! I'm very interested in React roles. 
           Could you share the job details, tech stack, and salary range?"
```

### Workflow 2: Recruiter Follow-up
```
Incoming: "Thanks for your interest. Can we schedule a call?"
You send:  "Draft a professional reply"
Assistant: "Absolutely! I'm available tomorrow at 3 PM or Thursday anytime. 
           Please send me the Zoom link. Looking forward to it!"
```

### Workflow 3: Quick Summary
```
Incoming: [long technical question about your experience]
You send:  "Summarize this message"
Assistant: "The sender is asking about your Docker and Django experience 
           for a potential project."
```

---

## 🔧 Available Commands

See **COMMANDS.md** for the complete list, but here are the main ones:

| Command | When to use |
|---------|------------|
| `summarize` | Understand what someone is asking |
| `draft` | Get a polished reply to send |
| `workflow` | Get both summary and draft together |
| Quick Action template | Use for specific scenarios (job, thanks, question, etc.) |

---

## 📝 Scenario Templates (10 total)

See **QUICK_ACTIONS.md** for templates and examples:

1. **Job Inquiry Response** — Recruiter or job offer
2. **Acknowledgment Reply** — Thanks and compliments
3. **Question Response** — Information requests
4. **Schedule/Meeting Response** — Meeting requests
5. **Project Collaboration Offer** — Work proposals
6. **Networking/Cold Outreach** — New connections
7. **Salary/Negotiation Inquiry** — Rate discussions
8. **Feedback/Code Review** — Review requests
9. **Urgent Request** — Time-sensitive help
10. **Professional Decline** — Turning down opportunities

---

## 🎓 Best Practices

- **Keep it short** — 2-4 sentences max per reply
- **Be professional** — Maintain your reputation
- **Always ask next steps** — Include a question or call to action
- **Review before sending** — Don't auto-send without checking
- **Mention skills when relevant** — React, Node.js, Django, Docker, etc.

---

## 🔗 Related Files

- Main SETUP_GUIDE: `../../SETUP_GUIDE.md`
- OpenClaw config: `../../setup/config/openclaw.json`
- Resume/profile: `../../data/resume.json`
- Environment template: `../../setup/.env.example`

---

## 📞 Troubleshooting

**OpenClaw not finding the skill?**
- Run `openclaw config validate`
- Check that skills are synced: `Copy-Item -Path "skills\*" -Destination "$env:USERPROFILE\.openclaw\skills" -Recurse -Force`

**DeepSeek API errors?**
- Verify your key in `~/.openclaw/.env` starts with `sk-`
- Check your account has credits: https://platform.deepseek.com/account/overview

**WhatsApp not connecting?**
- Open dashboard at `http://127.0.0.1:18789`
- Rescan the QR code in your WhatsApp app
- Make sure `WHATSAPP_NUMBER` matches your phone number

---

## 🚀 What's Next

Once WhatsApp is working:
1. Try different quick-action templates to see what works best
2. Add email automation (see `../../skills/email-manager`)
3. Set up job search automation (see `../../skills/job-hunt`)
4. Later: LinkedIn automation and voice replies

---

## 📋 Notes

- No OpenAI key required for text replies
- Voice transcription and TTS are optional (requires OpenAI key)
- All messages are logged to `../../data/applications_log.json`
- Never commit API keys to Git (use `.env` files)

---

**Happy automating! 🦞**
