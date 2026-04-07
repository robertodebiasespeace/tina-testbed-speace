#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Attiva/deattiva la delega temporanea per SafeProactive + WhatsApp Agent.
.DESCRIPTION
    Modifica safe-proactive/auto-rules.json per impostare lo stato di delega.
    Comandi:
        activate [-Mode <yield|routine|all>] [-TTLMinutes <int>]
        deactivate
        status
.PARAMETER Mode
    Modalità: 'yield' (solo yield), 'routine' (solo routine), 'all' (default)
.PARAMETER TTLMinutes
    Durata in minuti (default 30, max 60)
.EXAMPLE
    ./delegate-activate.ps1 activate -Mode all -TTLMinutes 30
#>

param(
    [Parameter(Mandatory=$false, Position=0)]
    [ValidateSet('activate','deactivate','status')]
    [string]$Action = 'status',

    [Parameter(Mandatory=$false)]
    [ValidateSet('yield','routine','all')]
    [string]$Mode = 'all',

    [Parameter(Mandatory=$false)]
    [ValidateRange(1,60)]
    [int]$TTLMinutes = 30
)

$workspace = Split-Path -Parent $PSScriptRoot
$rulesPath = Join-Path $workspace "auto-rules.json"

if (-not (Test-Path $rulesPath)) {
    Write-Host "❌ File auto-rules.json non trovato in safe-proactive/" -ForegroundColor Red
    exit 1
}

$rules = Get-Content $rulesPath -Raw | ConvertFrom-Json

switch ($Action) {
    'activate' {
        if ($rules.delegation_state.enabled) {
            Write-Host "⚠️ Delega già attiva. Rinnovo TTL a $TTLMinutes minuti." -ForegroundColor Yellow
        }
        $now = [datetime]::UtcNow
        $expires = $now.AddMinutes($TTLMinutes)
        $rules.delegation_state.enabled = $true
        $rules.delegation_state.activated_at = $now.ToString("yyyy-MM-ddTHH:mm:ssK")
        $rules.delegation_state.expires_at = $expires.ToString("yyyy-MM-ddTHH:mm:ssK")
        $rules.delegation_state.activated_by = "robertodebiase@outlook.it"
        $rules.delegation_state.mode = $Mode

        # Attiva le regole corrispondenti
        $rules.active_rules = @()
        foreach ($rule in $rules.rules) {
            $activate = $false
            if ($Mode -eq 'all') {
                $activate = $true
            }
            elseif ($Mode -eq 'yield' -and $rule.trigger -eq 'yield_opportunity') {
                $activate = $true
            }
            elseif ($Mode -eq 'routine' -and ($rule.trigger -in @('balance_inquiry','token_approve','monitoring_check'))) {
                $activate = $true
            }
            if ($activate) {
                $rule.activated_by = "robertodebiase@outlook.it"
                $rules.active_rules += $rule.id
            }
        }

        $rules | ConvertTo-Json -Depth 10 | Set-Content $rulesPath -Encoding UTF8
        Write-Host "✅ Delega attivata per $TTLMinutes minuti ($Mode). Regole attive:" -ForegroundColor Green
        $rules.active_rules | ForEach-Object { Write-Host "   • $_" }
    }

    'deactivate' {
        if (-not $rules.delegation_state.enabled) {
            Write-Host "ℹ️ Delega già disattivata." -ForegroundColor Cyan
            return
        }
        $rules.delegation_state.enabled = $false
        $rules.delegation_state.expires_at = $null
        $rules.delegation_state.activated_at = $null
        $rules.delegation_state.activated_by = $null
        $rules.delegation_state.mode = $null
        $rules.active_rules = @()

        $rules | ConvertTo-Json -Depth 10 | Set-Content $rulesPath -Encoding UTF8
        Write-Host "✅ Delega disattivata." -ForegroundColor Green
    }

    'status' {
        $state = $rules.delegation_state
        Write-Host "`n=== Delega Stato ===" -ForegroundColor Cyan
        Write-Host "Enabled: $($state.enabled)"
        Write-Host "Mode: $($state.mode)"
        Write-Host "Activated by: $($state.activated_by)"
        Write-Host "Expires at: $($state.expires_at)"
        Write-Host "Active rules: $($rules.active_rules.Count)"
        if ($state.enabled) {
            $now = [datetime]::UtcNow
            $exp = [datetime]::Parse($state.expires_at)
            $remaining = ($exp - $now).TotalMinutes
            Write-Host "TTL rimanente: $([math]::Round($remaining,1)) minuti" -ForegroundColor Yellow
        }
        Write-Host "`n=== Regole Disponibili ===" -ForegroundColor Cyan
        $rules.rules | ForEach-Object {
            $status = if ($rules.active_rules -contains $_.id) { "🟢" } else { "⚫" }
            Write-Host "$status $($_.id) — $($_.trigger) ($($_.ttl_minutes)min)"
        }
    }
}
