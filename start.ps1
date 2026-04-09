# ============================================================
# Quick Launch Script — Start the AI Assistant
# ============================================================
# Run this whenever you want to start/restart the assistant:
#   .\start.ps1
# ============================================================

Write-Host ""
Write-Host "🦞 Starting AI Personal Assistant..." -ForegroundColor Cyan
Write-Host ""

# ── Check if OpenClaw is installed ──────────────────────────
$openclawPath = Get-Command openclaw -ErrorAction SilentlyContinue
if (-not $openclawPath) {
    Write-Host "OpenClaw not found. Run setup\install.ps1 first." -ForegroundColor Red
    exit 1
}

# ── Deploy skills ────────────────────────────────────────────
$SkillsDir = "$env:USERPROFILE\.openclaw\skills"
Write-Host "Syncing skills..." -ForegroundColor Yellow
Copy-Item -Path "$PSScriptRoot\skills\*" -Destination $SkillsDir -Recurse -Force
Write-Host "  Skills synced ✓" -ForegroundColor Green

# ── Sync config ──────────────────────────────────────────────
$ConfigDest = "$env:USERPROFILE\.openclaw\openclaw.json"
if (-not (Test-Path $ConfigDest)) {
    Copy-Item "$PSScriptRoot\setup\config\openclaw.json" $ConfigDest
    Write-Host "  Config deployed ✓" -ForegroundColor Green
}

# ── Restart gateway ──────────────────────────────────────────
Write-Host "Restarting OpenClaw gateway..." -ForegroundColor Yellow
openclaw gateway restart
Write-Host "  Gateway running ✓" -ForegroundColor Green

# ── Open dashboard ───────────────────────────────────────────
Write-Host ""
Write-Host "✅ Assistant is running!" -ForegroundColor Green
Write-Host "   Dashboard: http://127.0.0.1:18789" -ForegroundColor Cyan
Write-Host "   WhatsApp: Send a message to test" -ForegroundColor Cyan
Write-Host ""
Write-Host "Opening dashboard in browser..." -ForegroundColor Yellow
Start-Process "http://127.0.0.1:18789"
