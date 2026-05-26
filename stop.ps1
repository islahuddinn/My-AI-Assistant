# ============================================================
# Stop the AI Assistant
# ============================================================

Write-Host ""
Write-Host "Stopping AI Personal Assistant..." -ForegroundColor Cyan
Write-Host ""

$openclawPath = Get-Command openclaw -ErrorAction SilentlyContinue
if (-not $openclawPath) {
    Write-Host "OpenClaw not found. Run setup\install.ps1 first." -ForegroundColor Red
    exit 1
}

Write-Host "Stopping OpenClaw gateway..." -ForegroundColor Yellow
try {
    openclaw gateway stop
    Write-Host "  Gateway stopped" -ForegroundColor Green
} catch {
    Write-Host "  Failed to stop gateway. It may already be stopped." -ForegroundColor DarkYellow
}

Write-Host ""
Write-Host "Assistant stop complete." -ForegroundColor Green
