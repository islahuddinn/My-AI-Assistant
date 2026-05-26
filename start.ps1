# ============================================================
# Quick Launch Script — Start the AI Assistant
# ============================================================
# Run this whenever you want to start/restart the assistant:
#   .\start.ps1
# ============================================================

Write-Host ""
Write-Host "Starting AI Personal Assistant..." -ForegroundColor Cyan
Write-Host ""

# Check if OpenClaw is installed
$openclawPath = Get-Command openclaw -ErrorAction SilentlyContinue
if (-not $openclawPath) {
    Write-Host "OpenClaw not found. Run setup\install.ps1 first." -ForegroundColor Red
    exit 1
}

# Deploy skills
$SkillsDir = "$env:USERPROFILE\.openclaw\skills"
if (-not (Test-Path $SkillsDir)) {
    New-Item -ItemType Directory -Path $SkillsDir -Force | Out-Null
}
Write-Host "Syncing skills..." -ForegroundColor Yellow
Copy-Item -Path "$PSScriptRoot\skills\*" -Destination $SkillsDir -Recurse -Force
Write-Host "  Skills synced" -ForegroundColor Green

# Sync config
$ConfigDest = "$env:USERPROFILE\.openclaw\openclaw.json"
$ConfigSource = "$PSScriptRoot\setup\config\openclaw.json"
if (-not (Test-Path $ConfigDest)) {
    Copy-Item $ConfigSource $ConfigDest -Force
    Write-Host "  Config deployed" -ForegroundColor Green
} else {
    Write-Host "  Config already exists — leaving it in place." -ForegroundColor DarkYellow
}

# Restart gateway
Write-Host "Restarting OpenClaw gateway..." -ForegroundColor Yellow
try {
    openclaw gateway restart
    Write-Host "  Gateway running" -ForegroundColor Green
} catch {
    Write-Host "  Gateway restart failed; starting gateway directly..." -ForegroundColor DarkYellow
    openclaw gateway run --port 18789 --bind loopback
}

# Open dashboard
Write-Host ""
Write-Host "Assistant is running (or starting)." -ForegroundColor Green
Write-Host "Gateway dashboard: http://127.0.0.1:18789" -ForegroundColor Cyan
Write-Host "If WhatsApp login is pending, open the dashboard and complete pairing." -ForegroundColor Cyan
Write-Host ""
Write-Host "Opening dashboard in browser..." -ForegroundColor Yellow
Start-Process "http://127.0.0.1:18789"
