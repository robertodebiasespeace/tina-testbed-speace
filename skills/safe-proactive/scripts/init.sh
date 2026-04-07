#!/bin/bash
# Initialization script for safe-proactive
# Sets up WAL, approval gates, and trusted device/user registries

echo "🔐 Initializing SafeProactive Agent..."

# Create workspace directories
mkdir -p ~/.openclaw/workspace/safe-proactive/{proposals,config,logs}

# Create WAL directory structure
mkdir -p ~/.openclaw/workspace/safe-proactive/proposals/WAL
mkdir -p ~/.openclaw/workspace/safe-proactive/proposals/APPROVED
mkdir -p ~/.openclaw/workspace/safe-proactive/proposals/REJECTED
mkdir -p ~/.openclaw/workspace/safe-proactive/proposals/SIMULATIONS

# Create proposal WAL template
if [ ! -f ~/.openclaw/workspace/safe-proactive/proposals/WAL_README.md ]; then
    cat > ~/.openclaw/workspace/safe-proactive/proposals/WAL_README.md << 'EOF'
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
EOF
fi

# Create trusted devices registry
if [ ! -f ~/.openclaw/workspace/safe-proactive/config/trusted_devices.json ]; then
    cat > ~/.openclaw/workspace/safe-proactive/config/trusted_devices.json << 'EOF'
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
EOF
    echo "🔑 Created trusted devices registry template at ~/.openclaw/workspace/safe-proactive/config/trusted_devices.json"
fi

# Create approved users registry
if [ ! -f ~/.openclaw/workspace/safe-proactive/config/approved_users.json ]; then
    cat > ~/.openclaw/workspace/safe-proactive/config/approved_users.json << 'EOF'
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
EOF
    echo "👤 Created approved users registry template at ~/.openclaw/workspace/safe-proactive/config/approved_users.json"
fi

# Create agent configuration
if [ ! -f ~/.openclaw/workspace/safe-proactive/agent-config.json ]; then
    cat > ~/.openclaw/workspace/safe-proactive/agent-config.json << 'EOF'
{
  "agent": {
    "name": "SafeProactive Agent",
    "version": "1.0.0",
    "enabled": true,
    "log_level": "INFO"
  },
  "wal": {
    "path": "~/.openclaw/workspace/safe-proactive/proposals/WAL",
    "max_entries_before_archive": 1000,
    "archive_path": "~/.openclaw/workspace/safe-proactive/proposals/WAL_ARCHIVE"
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
EOF
    echo "⚙️  Created agent config at ~/.openclaw/workspace/safe-proactive/agent-config.json"
fi

# Create empty log file
if [ ! -f ~/.openclaw/workspace/safe-proactive/logs/safe-proactive.log ]; then
    touch ~/.openclaw/workspace/safe-proactive/logs/safe-proactive.log
fi

echo "✅ SafeProactive Agent initialized!"
echo "📌 Next steps:"
echo "   1. Add your IoT devices to ~/.openclaw/workspace/safe-proactive/config/trusted_devices.json"
echo "   2. Verify approved users in ~/.openclaw/workspace/safe-proactive/config/approved_users.json"
echo "   3. Adjust thresholds in agent-config.json"
echo "   4. Run: openclaw skills start safe-proactive"

