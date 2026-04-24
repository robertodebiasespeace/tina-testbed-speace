#Requires -Version 5.1
<#
.SYNOPSIS
    Ferma il processo SPEACE in esecuzione in background.

.USAGE
    .\scripts\stop_speace_background.ps1
#>

[CmdletBinding()]
param()

Write-Host "[SPEACE Stopper] Ricerca processo SPEACE..." -ForegroundColor Cyan

# Cerca processi python che eseguono SPEACE-main.py
$pythonProcs = Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -match "SPEACE-main.py"
}

if (-not $pythonProcs) {
    Write-Host "[SPEACE Stopper] Nessun processo SPEACE trovato." -ForegroundColor Yellow
    exit 0
}

foreach ($proc in $pythonProcs) {
    Write-Host "[SPEACE Stopper] Terminazione processo python PID $($proc.Id)..."
    Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
}

Write-Host "[SPEACE Stopper] SPEACE arrestato." -ForegroundColor Green
