# SPEACE Setup Script (Windows PowerShell)
# Usage: .\setup.ps1 [-WithML] [-Force]

param(
    [switch]$WithML,
    [switch]$Force
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  SPEACE Framework - Setup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/4] Checking Python..." -ForegroundColor Yellow
$python = $null
foreach ($cmd in @("python3", "python")) {
    try {
        $v = & $cmd --version 2>&1
        if ($LASTEXITCODE -eq 0) { $python = $cmd; Write-Host "  Found: $v" -ForegroundColor Green; break }
    } catch {}
}
if (-not $python) {
    Write-Host "  ERROR: Python 3.10+ required. Install from https://python.org" -ForegroundColor Red
    exit 1
}

Write-Host "[2/4] Setting up virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    if ($Force) {
        Remove-Item -Recurse -Force "venv"
    } else {
        Write-Host "  venv exists. Use -Force to recreate." -ForegroundColor Cyan
    }
}
if (-not (Test-Path "venv")) {
    & $python -m venv venv
    Write-Host "  Created venv/" -ForegroundColor Green
}
. "venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip --quiet

Write-Host "[3/4] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
if ($WithML) {
    Write-Host "  Installing ML deps (~2GB, be patient)..." -ForegroundColor Magenta
    pip install -r requirements-ml.txt --quiet
}

Write-Host "[4/4] Finalizing..." -ForegroundColor Yellow
if (-not (Test-Path ".env") -and (Test-Path ".env.example")) {
    Copy-Item ".env.example" ".env"
    Write-Host "  Created .env from .env.example" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  SETUP COMPLETE" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Next: edit .env, then:" -ForegroundColor Gray
Write-Host "    python scripts/speace-cli.py" -ForegroundColor White
Write-Host "    python scripts/speace_autopilot.py" -ForegroundColor White
