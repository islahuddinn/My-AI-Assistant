# ============================================================
# Quick Launch Script — Start the AI Assistant
# ============================================================
# Run this whenever you want to start the assistant from this project:
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

# Copy the project .env to OpenClaw home if present
$RepoEnv = "$PSScriptRoot\.env"
$HomeEnv = "$env:USERPROFILE\.openclaw\.env"
if (Test-Path $RepoEnv) {
    Copy-Item -Path $RepoEnv -Destination $HomeEnv -Force
    Write-Host "  Copied project .env to OpenClaw home" -ForegroundColor Green

    $envContents = Get-Content $HomeEnv -ErrorAction SilentlyContinue
    $openRouterKey = $envContents | Where-Object { $_ -match '^OPENROUTER_API_KEY=' }
    if ($openRouterKey -and ($openRouterKey -replace '^OPENROUTER_API_KEY=', '').Trim() -eq '') {
        Write-Host "WARNING: OPENROUTER_API_KEY is empty in $HomeEnv." -ForegroundColor Yellow
        Write-Host "Add your OpenRouter API key before starting the assistant." -ForegroundColor Yellow
    }
} else {
    Write-Host "WARNING: No project .env found at $RepoEnv. OpenClaw may not have your API key." -ForegroundColor Yellow
}

# Launch the OpenClaw gateway in a new PowerShell window
Write-Host "Starting OpenClaw gateway in a new terminal..." -ForegroundColor Yellow
$gatewayCommand = "Set-Location -LiteralPath '$PSScriptRoot'; openclaw gateway run --port 18789 --bind loopback"
Start-Process powershell -ArgumentList @('-NoExit', '-Command', $gatewayCommand)

Write-Host "  Gateway launch requested." -ForegroundColor Green
Write-Host "  Dashboard will open shortly if the gateway starts successfully." -ForegroundColor Green
Start-Sleep -Seconds 4
Start-Process "http://127.0.0.1:18789"
