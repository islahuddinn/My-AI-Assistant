# AI Personal Assistant — Complete Setup & Usage Guide

## Overview
This is an AI-powered personal assistant that automates job hunting, LinkedIn management, email handling, and WhatsApp communication. It uses OpenClaw framework with DeepSeek AI.

## ⚠️ Important Warnings
- **LinkedIn TOS**: Automated job applications may violate LinkedIn's terms. Use at your own risk.
- **Security**: Protect your API keys and session files.
- **Rate Limits**: Tool includes built-in delays to avoid detection.

---

## Step-by-Step Setup Guide

### Step 1: Get API Keys
**Required: DeepSeek API Key** (nearly free AI brain)
1. Go to https://platform.deepseek.com/api_keys
2. Sign up and create an API key
3. Copy the key (starts with `sk-`)

**Optional: OpenAI API Key** (for voice note transcription)
1. Go to https://platform.openai.com/api-keys
2. Create key (~$0.006/minute for voice)

### Step 2: Install Dependencies
Run the one-time setup script:
```powershell
.\setup\install.ps1
```
This installs:
- Node.js and npm
- Python and pip
- OpenClaw framework
- Playwright browser automation
- Required Python packages

### Step 3: Configure API Keys
1. Copy the environment template:
```powershell
Copy-Item setup\.env.example "$env:USERPROFILE\.openclaw\.env"
```

2. Edit the `.env` file and add your real keys:
```
DEEPSEEK_API_KEY=sk-your-actual-deepseek-key-here
OPENAI_API_KEY=sk-your-openai-key-here  # optional
```

### Step 4: Fill Your Resume Data
Edit `data\resume.json` with your real information:
- Personal details (name, email, phone)
- Professional summary and experience
- Skills and education
- Job preferences

### Step 5: Onboard with OpenClaw
```powershell
openclaw onboard --non-interactive --mode local --auth-choice deepseek-api-key --deepseek-api-key "YOUR_DEEPSEEK_KEY" --skip-health --accept-risk
```

### Step 6: Deploy Skills and Config
```powershell
# Copy skills to OpenClaw
xcopy /E /I skills\* "%USERPROFILE%\.openclaw\skills\"

# Copy config
Copy-Item setup\config\openclaw.json "%USERPROFILE%\.openclaw\openclaw.json"
```

### Step 7: Start the Assistant
```powershell
.\start.ps1
```
This will:
- Sync skills and config
- Restart OpenClaw gateway
- Open dashboard at http://127.0.0.1:18789

### Step 8: Connect WhatsApp
1. In the dashboard, scan the WhatsApp QR code
2. Send a test message to yourself

### Step 9: Setup LinkedIn (First Time Only)
```powershell
python skills\linkedin-post\scripts\linkedin_post.py --login
```
- Browser opens — log in to LinkedIn
- Press ENTER in terminal after login
- Session is saved securely

---

## Daily Usage

### Starting the Assistant
```powershell
.\start.ps1
```

### WhatsApp Commands
Send these messages to your WhatsApp number:

**Job Hunting:**
- `find jobs: full stack developer remote`
- `apply all` (after reviewing jobs)
- `job digest` (manual daily digest)

**LinkedIn:**
- `post to linkedin: Your post content here`
- `find linkedin jobs: react developer`

**Email:**
- `check my email`
- `reply to email from john: Thanks for reaching out...`

**Voice Notes:**
- Send any voice note → auto-transcribed + replied
- Say "reply with voice" to get audio responses

**Utilities:**
- `status` — check system status
- `help` — list available commands

---

## Automation Training

### Cron Jobs (Daily Automation)
The system includes automated daily jobs in `automation/cron-daily-jobs.json`:

**Daily LinkedIn Digest (9 AM PKT):**
- Searches LinkedIn for remote developer jobs
- Sends top 5-8 jobs to WhatsApp
- Keywords: full stack, node.js, MERN, react developer remote

**Weekly Summary (Sunday 6 PM PKT):**
- Reports application statistics
- Suggests new searches if needed

### Standing Orders (Behavior Rules)
The assistant follows rules in `automation/standing-orders.md`:
- Always confirm destructive actions
- Only Easy Apply LinkedIn jobs
- Log all applications
- Professional communication
- Privacy protection

### Extending Automation
To add new automated tasks:
1. Edit `automation/cron-daily-jobs.json`
2. Add new cron job with schedule and message
3. The message will be sent to the assistant via WhatsApp

---

## Troubleshooting

### Common Issues

**OpenClaw not found:**
- Run `.\setup\install.ps1` again
- Check if Node.js is installed: `node --version`

**API Key errors:**
- Check `~\.openclaw\.env` file exists and has correct keys
- Verify keys start with `sk-`

**LinkedIn session expired:**
- Run `python skills\linkedin-post\scripts\linkedin_post.py --login` again

**WhatsApp not connecting:**
- Check dashboard at http://127.0.0.1:18789
- Rescan QR code

**Job applications failing:**
- Ensure resume.json is complete
- Check LinkedIn session is valid
- Verify Easy Apply jobs only

### Logs and Debugging
- Application logs: `data/applications_log.json`
- LinkedIn posts: `data/linkedin_posts_log.json`
- Debug screenshots: `data/debug_*.png` (auto-cleanup recommended)

---

## Security Best Practices

- Never commit `.env` files or session files to Git
- Keep `linkedin_session.json` and `gmail_token.json` secure
- Use strong, unique API keys
- Monitor LinkedIn account for unusual activity
- Regularly backup your configuration

---

## Cost Estimation
- **DeepSeek**: ~$0.001 per conversation (nearly free)
- **OpenAI**: ~$0.006/minute voice transcription (pennies/month)
- **Everything else**: Free (open source)

For personal use: < $1/month total.