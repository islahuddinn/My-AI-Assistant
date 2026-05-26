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

Write-Host "Stopping OpenClaw gateway service if present..." -ForegroundColor Yellow
try {
    openclaw gateway stop | Out-Null
    Write-Host "  Gateway service stop attempted." -ForegroundColor Green
} catch {
    Write-Host "  No gateway service to stop or service already removed." -ForegroundColor DarkYellow
}

Write-Host "Stopping any gateway listener on port 18789..." -ForegroundColor Yellow
$port = 18789
$connections = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
if ($connections) {
    $pids = $connections | Select-Object -ExpandProperty OwningProcess -Unique
    foreach ($pid in $pids) {
        try {
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
            Write-Host "  Stopped process PID $pid" -ForegroundColor Green
        } catch {
            Write-Host "  Failed to stop process PID $pid" -ForegroundColor DarkYellow
        }
    }
} else {
    Write-Host "  No gateway listener found on port $port." -ForegroundColor Green
}

Write-Host ""
Write-Host "Assistant stop complete." -ForegroundColor Green
