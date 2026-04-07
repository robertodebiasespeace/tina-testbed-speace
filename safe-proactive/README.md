# SafeProactive Agent

**Anticipate. Propose. Execute. Improve.**

An AI agent that continuously monitors your workspace, detects inefficiencies, and proposes improvements—all transparently, with your approval.

## 🎯 What It Does

### Continuous Monitoring
- 🔍 Scans workspace every 30 minutes
- 📊 Tracks metrics and performance
- 🚨 Detects anomalies immediately
- 📈 Learns from patterns

### Intelligent Analysis
- 🧠 Understands what's normal
- ⚠️ Identifies inefficiencies
- 💡 Spots opportunities
- 🎯 Prioritizes by risk level

### Safe Proposals
- 📋 Writes proposals before acting
- 👥 Waits for your approval
- 📖 Shows exact commands
- 🔒 Never obfuscates or hides

### Continuous Improvement
- 🔄 Learns from your decisions
- 📚 Improves recommendations over time
- 🎓 Shares insights via reports
- ✅ Tracks success metrics

## 🔐 Safety Model: Safe-WAL

**WAL** = Write-Ahead Logging

All actions follow this flow:

```
Discovery
    ↓
Analysis
    ↓
Scrub Sensitive Data
    ↓
Write to PROPOSALS.md
    ↓
Notify You
    ↓
WAIT FOR APPROVAL
    ↓
Execute
    ↓
Archive
```

**Guarantees**:
- ✅ Every action is readable
- ✅ Every command is proposed first
- ✅ No sensitive data is stored
- ✅ You have final approval authority
- ✅ Everything is auditable

## 📂 File Structure

```
~/.openclaw/workspace/safe-proactive/
├── SOUL.md                    - Agent identity & principles
├── AGENTS.md                  - Operational rules (Safe-WAL)
├── HEARTBEAT.md               - Monitoring & maintenance
├── PROPOSALS.md               - Active & pending proposals
├── agent-config.json          - Configuration
├── README.md                  - This file
├── heartbeat-log.json         - Heartbeat history
└── proposals-archive/         - Completed proposals
    ├── PROP-001-EXECUTED.md
    ├── PROP-002-REJECTED.md
    └── ...
```

## 🚀 How It Works

### Every 30 Minutes: Heartbeat

The agent wakes up and:

1. **Scans** - Check system state
2. **Analyzes** - Compare to baseline
3. **Detects** - Find anomalies
4. **Proposes** - Write to PROPOSALS.md
5. **Notifies** - Send WhatsApp alert
6. **Waits** - For your approval

### When You Decide

You have 3 options for each proposal:

```
✅ Approve PROP-XXX
   → Agent executes the command
   → Archives the proposal
   → Reports the outcome

❌ Reject PROP-XXX
   → Agent cancels the action
   → Archives as rejected
   → Records why you rejected it

❓ Clarify PROP-XXX: [question]
   → Agent provides more details
   → Updates the proposal
   → Waits for your decision
```

## 📋 Example Proposal

```markdown
## Proposal 001

**Title**: Archive old log files (>30 days)
**Risk Level**: Low
**Status**: Pending

### Why This Matters
Log directory is taking 500MB of storage.
Old logs (>30 days) are not accessed.
Archiving them saves space and keeps system responsive.

### What I'll Do
1. Find logs older than 30 days
2. Compress them to gzip
3. Move to archive directory
4. Remove original files
5. Enable automatic daily cleanup

### Exact Command
\`\`\`bash
# Find and compress logs older than 30 days
find ~/.openclaw/workspace/logs -type f -mtime +30 -exec gzip {} \;
# Move to archive
mv ~/.openclaw/workspace/logs/*.gz ~/.openclaw/workspace/safe-proactive/proposals-archive/logs-archived/

# Update logrotate config to auto-rotate daily
sed -i 's/rotate 7/rotate 7\n  daily/' /etc/logrotate.d/openclaw
\`\`\`

### Expected Outcome
- Log directory: 500MB → 50MB
- Old logs safely archived
- Automatic daily cleanup enabled
- System performance improved

### Potential Risks
- If an old log is unexpectedly needed, it's still in archive
- logrotate config change might affect other services

### Rollback Plan
\`\`\`bash
# Restore from archive
mkdir ~/.openclaw/workspace/logs-restored
mv ~/.openclaw/workspace/safe-proactive/proposals-archive/logs-archived/*.gz ~/.openclaw/workspace/logs-restored/
gunzip ~/.openclaw/workspace/logs-restored/*.gz

# Revert logrotate
sed -i 's/  daily//' /etc/logrotate.d/openclaw
\`\`\`

### Your Decision
- [x] Approved
- [ ] Rejected
- [ ] Needs clarification

**Comments**: Go ahead! We have the restored logs, so it's safe.
```

## 💡 Types of Proposals

### Low Risk ✅ (Propose & Inform)
- Documenting findings
- Creating non-sensitive configs
- Organizing files
- Generating reports

### Medium Risk ⚠️ (Propose & Wait)
- Config changes
- File deletions
- Dependency updates
- Permission changes

### High Risk 🔴 (Propose & Explain Carefully)
- System-level changes
- Database modifications
- Security settings
- Data deletion
- External integrations

## 🔔 WhatsApp Notifications

Every heartbeat, you receive updates like:

```
🫀 SafeProactive Heartbeat

Status: OK with 2 issues

📊 Metrics:
- Disk: 45% used
- Active Proposals: 1
- Last Issue: 2 hours ago

⚠️ Issues Found:
- Old config backup: config-2024-01-01.json

📋 Pending Proposals:
- PROP-002: Clean up old configs

💡 Next Steps:
Review and approve PROP-002 if you agree.

Next Heartbeat: in 30 minutes
---
SafeProactive v1.0
```

## 🎯 Example Workflow

### Day 1: Issue Detected
```
Heartbeat detects: Log file grew from 100MB to 350MB overnight
Proposal written: "Archive old logs" (PROP-001)
You receive: WhatsApp notification
```

### Day 1: Your Decision
```
You: "Approve PROP-001"
Agent: Executes the cleanup
Agent: Reports: "Freed 250MB. Logs now 100MB."
Agent: Archives PROP-001
```

### Day 2: Heartbeat Reports
```
You receive: "All clear! System performing well."
Agent: Continues monitoring
```

## 🛡️ What SafeProactive Can't Do

❌ Execute commands without proposal  
❌ Modify files silently  
❌ Delete anything automatically  
❌ Use obfuscated commands  
❌ Make "background" changes  
❌ Assume approval from silence  

## ✅ What SafeProactive Always Does

✅ Scans and analyzes  
✅ Proposes clearly  
✅ Shows exact commands  
✅ Waits for approval  
✅ Executes transparently  
✅ Archives for audit trail  

## 🔍 Monitoring Targets

The agent tracks:

### File System
- Log file sizes
- Disk space usage
- Old/unused files
- Directory structure

### Configuration
- Config changes
- Permission drift
- Settings consistency
- Backup status

### Performance
- Response times
- Tool failures
- Resource usage
- Baseline deviations

### Security
- Unexpected files
- Permission changes
- Suspicious patterns
- Config modifications

### Proposals
- Age of pending proposals
- Approval status
- Execution results
- Archived history

## 📊 Configuration

Edit `agent-config.json` to customize:

```json
{
  "heartbeat": {
    "interval_minutes": 30,
    "checks": {
      "file_system": true,
      "config_drift": true,
      "security": true
    }
  },
  "alert_thresholds": {
    "disk_usage_percent": 80,
    "log_file_size_mb": 500
  }
}
```

## 🎓 Learning Resources

1. **SOUL.md** - Understand the agent's identity and principles
2. **AGENTS.md** - Learn the Safe-WAL operational rules
3. **HEARTBEAT.md** - See how monitoring works
4. **PROPOSALS.md** - Approve/reject proposals

## 🚀 Getting Started

### Step 1: Understand the Philosophy
Read `SOUL.md` (5 minutes)

### Step 2: Learn the Rules
Read `AGENTS.md` (10 minutes)

### Step 3: See It In Action
Wait for first heartbeat (30 minutes)
You'll receive WhatsApp notification

### Step 4: Approve/Reject
React to proposals as they come

### Step 5: Let It Improve
Agent learns from your decisions

## 💬 Communication

SafeProactive communicates via:

- **WhatsApp**: Heartbeat updates and alerts
- **PROPOSALS.md**: Proposal tracking
- **Heartbeat-log.json**: Historical data
- **Proposals-archive/**: Completed proposals

## ✨ Key Principles

**1. Propose, Don't Execute**  
Every action is proposed first, never executed secretly.

**2. Transparency Over Speed**  
Show your work. Explain everything. Be honest about risks.

**3. Approval Authority**  
You make the final decision. Always.

**4. Audit Everything**  
Every action is logged and reversible.

**5. Continuous Learning**  
The agent improves based on your feedback.

## 🏆 Success Metrics

A successful SafeProactive setup:

- ✅ Issues detected early
- ✅ Proposals are actionable
- ✅ You understand every recommendation
- ✅ Problems get fixed proactively
- ✅ Your workspace stays healthy
- ✅ Zero surprises or hidden changes

## 🆘 Troubleshooting

### "I didn't get a heartbeat notification"
- Check WhatsApp is enabled in config
- Verify internet connection
- Check logs in `heartbeat-log.json`

### "A proposal doesn't make sense"
- Ask for clarification: `Clarify PROP-XXX: Why is this needed?`
- Agent will provide more details
- Reject if you disagree

### "I want to change settings"
- Edit `agent-config.json`
- Agent will notice and propose confirmation
- Changes take effect next heartbeat

---

## Summary

**SafeProactive** = Your proactive, transparent assistant

It finds problems before they become crises. It proposes solutions clearly. It waits for your approval. It improves continuously.

All without secrets. All with your control.

---

**SafeProactive Agent v1.0**  
**Principle**: Propose → Approve → Execute → Archive  
**Safety Model**: Safe-WAL (Write-Ahead Logging)  
**Authority**: You decide everything  

Ready to improve your workspace? Let's go! 🚀
