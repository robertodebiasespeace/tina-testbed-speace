# ============================================================
# SPEACE – Script Git Setup e Push GitHub Template
# Esegui in PowerShell dalla cartella SPEACE
#
# ISTRUZIONI:
# 1. Crea un Personal Access Token su GitHub: Settings → Developer settings → Personal access tokens
# 2. Sostituisci YOUR_GITHUB_TOKEN con il tuo token
# 3. Modifica GITHUB_USER con il tuo username GitHub
# 4. Modifica REPO_NAME con il nome del tuo repository
# 5. Esegui: .\scripts\setup\git-push-github.ps1
# 6. ELIMINA QUESTO FILE DOPO L'USO (per sicurezza)
# ============================================================

$GITHUB_TOKEN = "YOUR_GITHUB_TOKEN_HERE"  # <-- INSERISCI QUI IL TUO TOKEN
$GITHUB_USER  = "robertodebiasespeace"     # <-- MODIFICA CON IL TUO USERNAME
$REPO_NAME    = "tina-testbed-speace"       # <-- MODIFICA CON IL NOME REPO
$REPO_URL     = "https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${REPO_NAME}.git"
$SCRIPT_DIR   = Split-Path -Parent $MyInvocation.MyCommand.Path
$ROOT_DIR     = Split-Path -Parent (Split-Path -Parent $SCRIPT_DIR)

Write-Host "`n=== SPEACE GitHub Setup ===" -ForegroundColor Cyan
Write-Host "Cartella: $ROOT_DIR"
Set-Location $ROOT_DIR

# --- 1. Verifica repo GitHub ---
Write-Host "`n[1/5] Verifica repository GitHub..." -ForegroundColor Yellow
$headers = @{
    "Authorization" = "token $GITHUB_TOKEN"
    "Accept"        = "application/vnd.github.v3+json"
}
try {
    Invoke-WebRequest -Uri "https://api.github.com/repos/$GITHUB_USER/$REPO_NAME" `
        -Headers $headers -Method GET -UseBasicParsing | Out-Null
    Write-Host "     Repository esistente: OK" -ForegroundColor Green
} catch {
    Write-Host "     Creazione repository..." -ForegroundColor Yellow
    $body = @{
        name        = $REPO_NAME
        description = "SPEACE - SuPer Entita Autonoma Cibernetica Evolutiva | Rigene Project"
        private     = $false
        auto_init   = $false
    } | ConvertTo-Json
    try {
        Invoke-WebRequest -Uri "https://api.github.com/user/repos" `
            -Headers $headers -Method POST -Body $body `
            -ContentType "application/json" -UseBasicParsing | Out-Null
        Write-Host "     Repository creato!" -ForegroundColor Green
        Start-Sleep -Seconds 2
    } catch {
        Write-Host "     ERRORE creazione repo: $_" -ForegroundColor Red
    }
}

# --- 2. Inizializzazione git ---
Write-Host "`n[2/5] Inizializzazione git locale..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    & git init
    & git checkout -b main 2>$null
    if ($LASTEXITCODE -ne 0) {
        & git symbolic-ref HEAD refs/heads/main
    }
    Write-Host "     Repo git inizializzato su branch 'main'." -ForegroundColor Green
} else {
    Write-Host "     Repo git già esistente." -ForegroundColor Green
}

# --- 3. Configura utente ---
& git config user.email "robertodebiase80@gmail.com"
& git config user.name "Roberto De Biase"
Write-Host "     Utente configurato." -ForegroundColor Green

# --- 4. Stage e commit ---
Write-Host "`n[3/5] Stage e commit..." -ForegroundColor Yellow
& git add .
$status = & git status --short
if ($status) {
    & git commit -m "feat: SPEACE v1.2 Update

Aggiornamenti architettura:
- Adaptive Consciousness Framework (IIT+GWT+C-index)
- Agente Organismico Foundation (ST-6)
- AnythingLLM World Model Prototype
- Multi-Framework strategy
- Team Scientifico 7+ agenti
- SafeProactive governance

Alignment: 70.5/100
Fase: 1 Embrionale → Transition Fase 2

Fondatore: Roberto De Biase (rigeneproject.org)"
    Write-Host "     Commit creato." -ForegroundColor Green
} else {
    Write-Host "     Nessuna modifica da committare." -ForegroundColor Gray
}

# --- 5. Configura remote e push ---
Write-Host "`n[4/5] Configurazione remote GitHub..." -ForegroundColor Yellow
$remotes = & git remote
if ($remotes -contains "origin") {
    & git remote set-url origin $REPO_URL
} else {
    & git remote add origin $REPO_URL
}
Write-Host "     Remote origin configurato." -ForegroundColor Green

Write-Host "`n[5/5] Push su GitHub..." -ForegroundColor Yellow
& git push -u origin main
if ($LASTEXITCODE -eq 0) {
    Write-Host "`n=== PUSH COMPLETATO ===" -ForegroundColor Green
    Write-Host "Repository: https://github.com/$GITHUB_USER/$REPO_NAME" -ForegroundColor Cyan
} else {
    Write-Host "`nATTENZIONE: Push fallito." -ForegroundColor Red
    Write-Host "Prova manualmente: git push -u origin main" -ForegroundColor Yellow
}

# Pulizia token dalla config git
& git remote set-url origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
Write-Host "`nToken rimosso dalla config git locale." -ForegroundColor Gray
Write-Host "ELIMINA QUESTO FILE dopo l'uso per sicurezza!" -ForegroundColor DarkYellow
