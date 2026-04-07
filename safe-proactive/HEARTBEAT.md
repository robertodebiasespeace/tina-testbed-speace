# HEARTBEAT.md - SafeProactive Monitoring & Maintenance

## Heartbeat Schedule

**Frequency**: Every 30 minutes (configurable)  
**Purpose**: Detect anomalies, identify inefficiencies, propose improvements

## What Gets Checked

### 1. File System Health
- **Check**: Log file sizes (growing unexpectedly?)
- **Check**: Temp files accumulation
- **Check**: Disk space usage trends
- **Action**: Propose cleanup if >80% used
- **Frequency**: Every heartbeat

### 2. Configuration Drift
- **Check**: Config files match baseline
- **Check**: Permissions still correct
- **Check**: Settings haven't changed unexpectedly
- **Action**: Propose sync if drift detected
- **Frequency**: Every heartbeat

### 3. Workspace Organization
- **Check**: Memory files are accessible
- **Check**: Old logs can be archived
- **Check**: Directories are clean
- **Action**: Propose organization if cluttered
- **Frequency**: Daily

### 4. Performance Metrics
- **Check**: Response times normal?
- **Check**: Any tools failing?
- **Check**: Resource usage patterns
- **Action**: Propose optimization if degraded
- **Frequency**: Every heartbeat

### 5. Security Baseline
- **Check**: No unexpected files created
- **Check**: File permissions normal
- **Check**: Config files unchanged
- **Action**: Propose investigation if anomaly
- **Frequency**: Every heartbeat

### 6. Proposal Backlog
- **Check**: Any pending proposals?
- **Check**: How old are they?
- **Check**: User feedback status
- **Action**: Remind about pending approvals
- **Frequency**: Every heartbeat

## Heartbeat Actions

### Inform (Always Safe)
✅ Report findings via WhatsApp  
✅ Show metrics and trends  
✅ Explain what's changing  
✅ Show performance

### Propose (Safe-WAL Compliant)
✅ Write new proposals to PROPOSALS.md  
✅ Include full analysis  
✅ Show exact command  
✅ Wait for approval  

### Archive (Only if Approved)
✅ Move executed proposals  
✅ Keep audit trail clean  
✅ Track completion  

## Heartbeat Notification Format

When heart beats, you'll receive:

```
🫀 SafeProactive Heartbeat

Status: OK / ISSUES FOUND

📊 Metrics:
- Disk Usage: 45%
- Active Proposals: 2
- Last Issue: 6 hours ago

⚠️ Issues Detected:
- Log file growing fast: /logs/app.log (250MB)
- Unused config: old_backup.conf

📋 Pending Proposals:
- PROP-001: Archive old logs
- PROP-003: Clean temp files

💡 Recommendations:
1. Review and approve PROP-001
2. Consider enabling auto-cleanup

Next Heartbeat: in 30 minutes
---
SafeProactive v1.0
```

## Anomaly Detection

If I detect something unusual, I:

1. **Analyze** - What is this? Is it normal?
2. **Baseline** - How does it compare to history?
3. **Risk** - What could go wrong?
4. **Propose** - Write proposal with solution
5. **Alert** - Notify you immediately (don't wait for next heartbeat)

## Example Heartbeat Scenarios

### Scenario 1: Log File Growing
```
Detected: /logs/app.log = 500MB (was 100MB yesterday)

Analysis: Growth rate is 5x normal
Proposal: Archive old logs and enable rotation
Risk: Low
Status: Pending your approval

Command:
  1. Rotate current log
  2. Compress old logs
  3. Enable daily rotation in config
```

### Scenario 2: Config Drift
```
Detected: TIMEOUT in config.json changed from 30 to 60 (unauthorized?)

Analysis: This is unusual - you didn't mention changing it
Proposal: Revert to 30 seconds (original)
Risk: Medium (could break something if 60s is needed)
Status: Waiting for your input

What should I do?
1. Revert to 30
2. Keep 60 and update baseline
3. Investigate what changed
```

### Scenario 3: Pending Proposals Age
```
Detected: PROP-001 has been pending for 48 hours

Analysis: Might be forgotten or awaiting clarification
Notification: "PROP-001 is waiting for your approval. Need more info?"
```

## Configuration

### Edit Heartbeat Behavior

```json
{
  "heartbeat": {
    "enabled": true,
    "interval_minutes": 30,
    "checks": {
      "file_system": true,
      "config_drift": true,
      "security": true,
      "performance": true,
      "proposals": true
    },
    "alert_thresholds": {
      "disk_usage_percent": 80,
      "log_file_size_mb": 500,
      "old_proposals_hours": 48
    },
    "notification_channel": "whatsapp",
    "summary_frequency": "daily"
  }
}
```

## What NOT to Do During Heartbeat

❌ Execute commands without proposal  
❌ Modify config files silently  
❌ Delete anything automatically  
❌ Make background changes  
❌ Assume approval from silence  

## What TO Do During Heartbeat

✅ Scan and analyze  
✅ Detect anomalies  
✅ Write proposals  
✅ Notify about findings  
✅ Wait for approval  
✅ Report results  

## Heartbeat Workflow

```
Heartbeat Triggers
    ↓
Scan System State
    ↓
Detect Anomalies
    ↓
├─ Low Risk → Propose and inform
├─ Medium Risk → Propose and wait
├─ High Risk → Alert and propose carefully
└─ No Issues → Report "All Clear"
    ↓
Write to PROPOSALS.md (if needed)
    ↓
Send Notification
    ↓
Wait for Your Response (if applicable)
    ↓
Archive Proposals (once approved/executed)
```

## Emergency Override

If heartbeat detects something that requires **immediate** action to prevent damage:

1. **Propose immediately** (don't wait for next heartbeat)
2. **Execute with warning** (show what I'm about to do)
3. **Notify instantly** (not in regular report)
4. **Log everything** (so you can review)
5. **Ask for feedback** (did I do the right thing?)

Examples of immediate threats:
- 🔴 Disk 100% full (about to crash)
- 🔴 Security breach detected
- 🔴 Critical system failure

Normal issues (wait for approval):
- 🟡 Config drift
- 🟡 Large log files
- 🟡 Old temporary files

## Success Metrics

A successful heartbeat:

- ✅ Detected real issues
- ✅ Proposed clear solutions
- ✅ Waited for approval
- ✅ Executed cleanly
- ✅ Reported results
- ✅ Updated baseline

A failed heartbeat:

- ❌ Executed without proposal
- ❌ Didn't notify
- ❌ Made risky changes
- ❌ Couldn't rollback

## Heartbeat History

Every heartbeat is logged in:  
`~/.openclaw/workspace/safe-proactive/heartbeat-log.json`

```json
{
  "heartbeat_001": {
    "timestamp": "2026-03-25T10:00:00Z",
    "duration_seconds": 45,
    "checks_completed": 6,
    "anomalies_found": 2,
    "proposals_created": 1,
    "status": "completed"
  }
}
```

---

## Summary

**Heartbeat** = Continuous, safe monitoring  
**Safe-WAL** = Propose before executing  
**Proposals** = Your approval authority  
**Transparency** = You see everything  

The heartbeat keeps the system healthy without surprising you.

---

**SafeProactive Agent v1.0**  
**Monitoring**: Continuous  
**Acting**: Only with approval  
**Transparency**: Complete  
