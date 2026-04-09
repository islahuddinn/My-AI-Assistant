# ============================================================
# AI Assistant Setup Script — OpenClaw on Windows
# ============================================================
# Run this from the project root:
#   .\setup\install.ps1
# ============================================================

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$OpenClawSkillsDir = "$env:USERPROFILE\.openclaw\skills"
$OpenClawConfigDir = "$env:USERPROFILE\.openclaw"

Write-Host ""
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "   AI Personal Assistant — Setup Script" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

# ─── Step 1: Check Node.js ─────────────────────────────────
Write-Host "[1/6] Checking Node.js..." -ForegroundColor Yellow
$nodeVersion = node --version 2>$null
if (-not $nodeVersion) {
    Write-Host "  Node.js not found. Installing via winget..." -ForegroundColor Red
    winget install OpenJS.NodeJS.LTS --silent
    Write-Host "  Node.js installed. Please restart this script." -ForegroundColor Green
    exit 0
} else {
    Write-Host "  Node.js $nodeVersion found ✓" -ForegroundColor Green
}

# ─── Step 2: Check Python ──────────────────────────────────
Write-Host "[2/6] Checking Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>$null
if (-not $pythonVersion) {
    Write-Host "  Python not found. Installing via winget..." -ForegroundColor Red
    winget install Python.Python.3.11 --silent
    Write-Host "  Python installed. Please restart this script." -ForegroundColor Green
    exit 0
} else {
    Write-Host "  $pythonVersion found ✓" -ForegroundColor Green
}

# ─── Step 3: Install OpenClaw ──────────────────────────────
Write-Host "[3/6] Installing OpenClaw..." -ForegroundColor Yellow
$existingOpenClaw = npm list -g openclaw 2>$null
if ($existingOpenClaw -match "openclaw@") {
    Write-Host "  OpenClaw already installed ✓" -ForegroundColor Green
} else {
    npm install -g openclaw@latest
    Write-Host "  OpenClaw installed ✓" -ForegroundColor Green
}

# ─── Step 4: Install Python dependencies ───────────────────
Write-Host "[4/6] Installing Python dependencies..." -ForegroundColor Yellow
pip install --quiet `
    playwright `
    google-auth `
    google-auth-oauthlib `
    google-auth-httplib2 `
    google-api-python-client `
    requests `
    feedparser `
    python-dotenv `
    colorama

# Install Playwright browsers
playwright install chromium
Write-Host "  Python dependencies installed ✓" -ForegroundColor Green

# ─── Step 5: Copy skills to OpenClaw ───────────────────────
Write-Host "[5/6] Deploying skills to OpenClaw..." -ForegroundColor Yellow
if (-not (Test-Path $OpenClawSkillsDir)) {
    New-Item -ItemType Directory -Path $OpenClawSkillsDir -Force | Out-Null
}

$SkillsSource = "$ProjectRoot\skills"
if (Test-Path $SkillsSource) {
    Copy-Item -Path "$SkillsSource\*" -Destination $OpenClawSkillsDir -Recurse -Force
    Write-Host "  Skills deployed to $OpenClawSkillsDir ✓" -ForegroundColor Green
} else {
    Write-Host "  Skills directory not found, skipping..." -ForegroundColor DarkYellow
}

# ─── Step 6: Copy config (if openclaw.json doesn't exist) ──
Write-Host "[6/6] Configuring OpenClaw..." -ForegroundColor Yellow
$ConfigTarget = "$OpenClawConfigDir\openclaw.json"
$ConfigSource = "$ProjectRoot\setup\config\openclaw.json"

if (-not (Test-Path $ConfigTarget)) {
    if (Test-Path $ConfigSource) {
        Copy-Item -Path $ConfigSource -Destination $ConfigTarget -Force
        Write-Host "  Config copied ✓" -ForegroundColor Green
    }
} else {
    Write-Host "  Config already exists — skipping (edit manually if needed)" -ForegroundColor DarkYellow
}

# ─── Done ──────────────────────────────────────────────────
Write-Host ""
Write-Host "=====================================================" -ForegroundColor Green
Write-Host "   Setup Complete!" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Edit setup\config\openclaw.json — add your API keys & phone number"
Write-Host "  2. Edit data\resume.json — add your profile for job applications"
Write-Host "  3. Run: openclaw onboard --install-daemon"
Write-Host "  4. Run: openclaw dashboard   (then scan WhatsApp QR)"
Write-Host "  5. Send a message to your Telegram bot to test!"
Write-Host ""
