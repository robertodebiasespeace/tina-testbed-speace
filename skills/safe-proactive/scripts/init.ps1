# Initialization script for safe-proactive (PowerShell version)
# Sets up WAL, approval gates, and trusted device/user registries

Write-Host "[INFO] Initializing SafeProactive Agent..." -ForegroundColor Cyan

# Create workspace directories
$base = "$env:USERPROFILE\.openclaw\workspace\safe-proactive"
New-Item -ItemType Directory -Path "$base\proposals\WAL" -Force | Out-Null
New-Item -ItemType Directory -Path "$base\proposals\APPROVED" -Force | Out-Null
New-Item -ItemType Directory -Path "$base\proposals\REJECTED" -Force | Out-Null
New-Item -ItemType Directory -Path "$base\proposals\SIMULATIONS" -Force | Out-Null
New-Item -ItemType Directory -Path "$base\config" -Force | Out-Null
New-Item -ItemType Directory -Path "$base\logs" -Force | Out-Null

# Create proposal WAL template
$walReadme = "$base\proposals\WAL_README.md"
if (-not (Test-Path $walReadme)) {
    $content = @'
# Write-Ahead Log (WAL) for SafeProactive

All autonomous proposals are logged here BEFORE execution.

## File Naming Convention
WAL_YYYY-MM-DD_HHMMSS_ID.md

## Content Structure
- Proposal ID and timestamp
- Self-Location (ITI + SEA)
- Constraints mapping (validated)
- Push signal details
- Proposed action with reasoning
- Safety assessment (stack level, reversibility)
- Approval status (PENDING/APPROVED/REJECTED/AUTO)
- Outcome log (after execution)

## Integrity
WAL files are append-only. Do not modify after creation.

## Retention
Keep all WAL entries permanently for audit purposes.
Archive old entries to WAL_ARCHIVE/ after 1000 entries.
'@
    Set-Content -Path $walReadme -Value $content -Encoding UTF8
    Write-Host "[OK] Created WAL README at $walReadme" -ForegroundColor Green
}

# Create trusted devices registry
$devicesFile = "$base\config\trusted_devices.json"
if (-not (Test-Path $devicesFile)) {
    $content = @'
{
  "registry_version": "1.0",
  "devices": {
    "example_thermostat": {
      "device_id": "thermostat_livingroom_01",
      "name": "Living Room Thermostat",
      "type": "iot_sensor",
      "public_key_fingerprint": "AB:CD:EF:12:34:56:78:90",
      "allowed_events": ["temperature_update", "humidity_update", "mode_change"],
      "max_frequency_hz": 0.1,
      "trust_level": "high"
    }
  },
  "notes": "Add your IoT devices here. Never trust devices without cryptographic signatures."
}
'@
    Set-Content -Path $devicesFile -Value $content -Encoding UTF8
    Write-Host "[OK] Created trusted devices registry template at $devicesFile" -ForegroundColor Green
}

# Create approved users registry
$usersFile = "$base\config\approved_users.json"
if (-not (Test-Path $usersFile)) {
    $content = @'
{
  "registry_version": "1.0",
  "users": {
    "roberto": {
      "user_id": "roberto",
      "name": "Roberto",
      "whatsapp": "+393714191412",
      "approval_method": "whatsapp",
      "max_proposal_level": 3,
      "timeout_seconds": 600,
      "auto_approve_level1": true
    }
  },
  "default_policy": {
    "require_approval_for_level2": true,
    "require_approval_for_level3": true,
    "simulation_required_for_self_edit": true,
    "max_pending_proposals": 10
  }
}
'@
    Set-Content -Path $usersFile -Value $content -Encoding UTF8
    Write-Host "[OK] Created approved users registry template at $usersFile" -ForegroundColor Green
}

# Create agent configuration
$agentConfig = "$base\agent-config.json"
if (-not (Test-Path $agentConfig)) {
    $content = @'
{
  "agent": {
    "name": "SafeProactive Agent",
    "version": "1.0.0",
    "enabled": true,
    "log_level": "INFO"
  },
  "wal": {
    "path": "$env:USERPROFILE\.openclaw\workspace\safe-proactive\proposals\WAL",
    "max_entries_before_archive": 1000,
    "archive_path": "$env:USERPROFILE\.openclaw\workspace\safe-proactive\proposals\WAL_ARCHIVE"
  },
  "approval": {
    "timeout_seconds": 600,
    "escalation_enabled": true,
    "notify_on_timeout": true
  },
  "push_validation": {
    "enabled": true,
    "require_device_signatures": true,
    "user_whitelist_enabled": true,
    "reject_unknown_sources": true
  },
  "constraint_validator": {
    "enabled": true,
    "auto_downgrade_on_unconfirmed": true,
    "conflict_detection": true,
    "halt_on_level0_threat": true
  },
  "simulation": {
    "enabled_for_self_edit": true,
    "historical_cycles": 100,
    "safety_metric_threshold": 0.95
  },
  "notification": {
    "channel": "whatsapp",
    "approval_requests_to": "+393714191412",
    "status_updates": true
  }
}
'@
    Set-Content -Path $agentConfig -Value $content -Encoding UTF8
    Write-Host "[OK] Created agent config at $agentConfig" -ForegroundColor Green
}

# Create empty log file
$logFile = "$base\logs\safe-proactive.log"
if (-not (Test-Path $logFile)) {
    New-Item -ItemType File -Path $logFile -Force | Out-Null
}

Write-Host "[SUCCESS] SafeProactive Agent initialized!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Add your IoT devices to $devicesFile"
Write-Host "  2. Verify approved users in $usersFile"
Write-Host "  3. Adjust thresholds in $agentConfig"
Write-Host "  4. Run: openclaw skills start safe-proactive"
Write-Host ""
