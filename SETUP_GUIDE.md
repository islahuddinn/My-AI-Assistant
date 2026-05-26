# AI Personal Assistant — Complete Setup & Usage Guide

## Overview
This is an AI-powered personal assistant that automates job hunting, LinkedIn management, email handling, and WhatsApp communication. It uses the OpenClaw framework with a free OpenRouter model.

## ⚠️ Important Warnings
- **LinkedIn TOS**: Automated job applications may violate LinkedIn's terms. Use at your own risk.
- **Security**: Protect your API keys and session files.
- **Rate Limits**: Tool includes built-in delays to avoid detection.

---

## CI / CD (Optional)

You can add a simple CI that checks Python syntax and installs dependencies. A minimal GitHub Actions workflow has been added at `.github/workflows/ci.yml` which:

- Installs Python 3.11
- Installs the packages from `requirements.txt`
- Installs Playwright browsers
- Runs `python -m py_compile` across the repository to catch syntax errors

To enable automatic deployment (CD) you'll need to add packaging and deployment steps tailored to your target environment (Docker image push, remote VM deploy, cloud function, etc.). If you want, I can scaffold a Docker-based deployment workflow next.

## Training / Model

- No local model training is required. The assistant uses hosted models via OpenRouter (`OPENROUTER_API_KEY`) and optional OpenAI for voice transcription. There is no separate training step to run locally.

## WhatsApp env variable added

I added your WhatsApp number to the env template `setup/.env.example` as `WHATSAPP_NUMBER=+923036039298`. Copy the example to your OpenClaw env location and edit if needed:

```powershell
Copy-Item setup\.env.example "$env:USERPROFILE\.openclaw\.env"
notepad "$env:USERPROFILE\.openclaw\.env"
```

OpenClaw reads `setup/config/openclaw.json` for the `channels.whatsapp.allowFrom` list (it already includes your number). The `WHATSAPP_NUMBER` env variable is provided so you can centralize settings; ensure the number in `openclaw.json` matches the env variable if you change it.


## Step-by-Step Setup Guide

### Step 1: Get API Keys
**Required: OpenRouter API Key** (free-tier AI brain)
1. Go to https://openrouter.ai
2. Sign up and create an API key
3. Copy the key (starts with `or-`)

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
OPENROUTER_API_KEY=or-your-openrouter-key-here
OPENAI_API_KEY=sk-your-openai-key-here  # optional
```

### Step 4: Fill Your Resume Data
Edit `data\resume.json` with your real information:
- Personal details (name, email, phone)
- Professional summary and experience
- Skills and education
- Job preferences

### Step 5: Onboard with OpenClaw
This repository is configured to use the local gateway only, so you do not need to install a daemon or auto-start the service.

If you previously installed a gateway service, run:
```powershell
openclaw gateway uninstall
```

Then start the assistant with:
```powershell
.\start.ps1
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
- **OpenRouter**: free tier available for owl-alpha and other supported models
- **OpenAI**: ~$0.006/minute voice transcription (pennies/month)
- **Everything else**: Free (open source)

For personal use: < $1/month total.