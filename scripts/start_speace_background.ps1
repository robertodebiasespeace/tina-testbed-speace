#Requires -Version 5.1
<#
.SYNOPSIS
    Avvia SPEACE in background continuo con log in tempo reale.

.DESCRIPTION
    Lancia python SPEACE-main.py --continuous in background tramite
    Start-Process (processo indipendente), redirige l'output su un file
    di log nella cartella logs/, e apre una finestra PowerShell dedicata
    per visualizzare il log in tempo reale.

.USAGE
    Da PowerShell nella cartella del progetto:
        .\scripts\start_speace_background.ps1

    Per fermare SPEACE:
        .\scripts\stop_speace_background.ps1
#>

[CmdletBinding()]
param(
    [switch]$LogViewer = $true,
    [string]$LogFile = "logs/speace_continuous.log"
)

# ---------------------------------------------------------------------------
# Configurazione
# ---------------------------------------------------------------------------
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$LogPath     = Join-Path $ProjectRoot $LogFile
$LogDir      = Split-Path -Parent $LogPath

# Crea la cartella logs se manca
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

# ---------------------------------------------------------------------------
# Verifica processo esistente
# ---------------------------------------------------------------------------
$existing = Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -match "SPEACE-main.py"
}
if ($existing) {
    Write-Host "[SPEACE Launcher] Processo SPEACE gia' in esecuzione (PID $($existing.Id))." -ForegroundColor Yellow
    Write-Host "  Per fermare: .\scripts\stop_speace_background.ps1"
    if ($LogViewer) {
        Write-Host "[SPEACE Launcher] Apro il log viewer..."
        Start-Process powershell -ArgumentList "-NoExit","-Command","Get-Content '$LogPath' -Wait -Tail 20"
    }
    exit 0
}

# ---------------------------------------------------------------------------
# Avvio processo in background (redirezione nativa su file)
# ---------------------------------------------------------------------------
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  SPEACE Background Launcher" -ForegroundColor Cyan
Write-Host "  Progetto: $ProjectRoot" -ForegroundColor Cyan
Write-Host "  Log file: $LogPath" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Usa cmd /c per redirezione nativa stdout/stderr su file (flush immediato)
$cmd = "python -u SPEACE-main.py --continuous > `"$LogPath`" 2>&1"
Start-Process cmd -ArgumentList "/c", $cmd -WorkingDirectory $ProjectRoot -WindowStyle Hidden

Write-Host "[SPEACE Launcher] Processo avviato in background." -ForegroundColor Green
Write-Host ""

# Attendi un attimo che il processo scriva il banner
Start-Sleep -Seconds 2

# ---------------------------------------------------------------------------
# Apri log viewer in finestra dedicata
# ---------------------------------------------------------------------------
if ($LogViewer) {
    Write-Host "[SPEACE Launcher] Apertura finestra log viewer..."
    $viewerCmd = "Get-Content '$LogPath' -Wait -Tail 20"
    Start-Process powershell -ArgumentList "-NoExit","-Command",$viewerCmd
    Write-Host ""
}

# ---------------------------------------------------------------------------
# Istruzioni operative
# ---------------------------------------------------------------------------
Write-Host "--- Operazioni disponibili ---" -ForegroundColor Yellow
Write-Host "  Fermare SPEACE:    .\scripts\stop_speace_background.ps1"
Write-Host "  Leggere log:       Get-Content '$LogPath' -Wait -Tail 20"
Write-Host ""
Write-Host "[SPEACE Launcher] SPEACE e' in esecuzione in background." -ForegroundColor Green
