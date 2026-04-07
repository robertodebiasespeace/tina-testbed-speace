# AGENTS.md — SafeProactive Operational Routines

## 🤖 What This File Is For

This file defines **how SafeProactive operates in the background**. It's the operational playbook for:
- Heartbeat monitoring (periodic checks)
- Routine maintenance tasks
- Emergency escalation procedures
- Performance optimization

Think of it as your agent's daily operations checklist.

---

## 💓 Heartbeat Protocol (Every 30 Minutes)

When a heartbeat is triggered, run through this checklist:

### Heartbeat Check 1: WAL Integrity

**Command:** `Check WAL for tampering`

```bash
# Verify no WAL entries were deleted or modified
# Check checksums (if implemented)
# Compare proposal count to execution count
```

**What to look for:**
- New WAL entries exist (proposals are being logged)
- Execution log matches approval log
- No gaps in proposal IDs (sequential numbering)

**If failed:**
- Log security incident
- Alert operator
- Enter "audit mode" (increase human approval threshold)

---

### Heartbeat Check 2: Constraint Consistency

**Command:** `Analyze recent constraint mappings`

```bash
# Extract constraints from last 10 WAL entries
# Check for contradictions (e.g., "battery low" vs. "battery stable")
# Verify constraint priorities are consistent
```

**What to look for:**
- Constraints are logically consistent
- Priority ordering hasn't drifted
- Level 0 (Integrity) violations don't occur repeatedly

**If problem found:**
- Log the inconsistency
- Adjust constraint mapping if simple fix
- Escalate to human if complex

---

### Heartbeat Check 3: Push Signal Validation Rate

**Command:** `Analyze semantic validation success rate`

```bash
# Count push signals processed in last 30 minutes
# Count signals rejected by validation
# Calculate rejection rate
```

**What to look for:**
- Rejection rate is <5% (normal signal noise)
- No cascade of suspicious signals
- No repeated attacks from same source

**If rejection rate >10%:**
- Check for attack pattern (same source?)
- Log security incident
- Increase validation strictness
- Alert operator

---

### Heartbeat Check 4: Approval Log Review

**Command:** `Check Level 2+ approvals`

```bash
# List all approvals granted in last 30 minutes
# Verify human operator approved each one
# Check timeout didn't expire (auto-reject)
```

**What to look for:**
- All Level 2 approvals have human signature
- No auto-rejections due to timeout
- Approved actions completed successfully

**If approval issue found:**
- Investigate why approval failed
- Retry or escalate
- Log the issue

---

### Heartbeat Check 5: Resource Usage Trends

**Command:** `Monitor CPU, memory, bandwidth`

```bash
# Check recent resource utilization
# Compare to baseline
# Detect anomalies
```

**What to look for:**
- CPU <80%
- Memory <75%
- No runaway processes
- No resource leaks

**If threshold exceeded:**
- Activate low-power mode
- Reduce exploration intensity
- Alert operator if critical

---

### Heartbeat Check 6: Decision Pattern Analysis

**Command:** `Detect alignment drift`

```bash
# Analyze decisions from last 100 cycles
# Check if goal/motivation is shifting
# Compare to baseline from first 100 cycles
```

**What to look for:**
- Goal stability (decisions still aligned with initial values)
- No systematic drift toward boundary-breaking
- Intrinsic motivation rewards remain balanced

**If drift detected:**
- Log the suspected drift
- Request human review
- Temporarily increase approval requirements
- Provide decision diff to operator

---

## 🛠️ Maintenance Tasks (Hourly)

### Maintenance Task 1: WAL Rotation

**When:** Every 1 hour or when WAL size exceeds 10MB

**Action:**
```bash
# Archive old WAL entries (older than 24h)
# Move to WAL_archive/
# Keep current WAL <10MB for performance
```

**Outcome:** WAL stays manageable; old entries preserved for audit.

---

### Maintenance Task 2: Approval Log Cleanup

**When:** Every 1 hour

**Action:**
```bash
# Review rejected proposals (older than 24h)
# If no new context, archive them
# Keep recent rejections visible for analysis
```

**Outcome:** Approval log stays readable; decisions remain auditable.

---

### Maintenance Task 3: Memory Optimization

**When:** Every 1 hour or on resource pressure

**Action:**
```bash
# Compress memory/ directory (gzip old files)
# Remove duplicate log entries
# Keep recent state (last 10 cycles) uncompressed
```

**Outcome:** Memory usage stable; state recovery fast.

---

## 🚨 Emergency Escalation (Automatic)

These events trigger **immediate human notification** (no heartbeat required):

### Escalation 1: Level 0 Violation

**Trigger:** Safety constraint violated (e.g., battery critical, network down, physical safety threatened)

**Action:**
1. Halt all Level 2+ operations
2. Log emergency
3. Send **URGENT** notification to operator
4. Enter emergency mode (minimal operation, wait for human)

**Message to operator:**
```
🚨 SAFETY ALERT 🚨
Level 0 (Integrity) violation detected.
Timestamp: [TIME]
Cause: [SPECIFIC ISSUE]
Agent Status: HALTED (awaiting human decision)
Action required: [SPECIFIC ACTION]
```

---

### Escalation 2: Semantic Validation Cascade

**Trigger:** >3 push signals rejected in 1 minute (potential attack)

**Action:**
1. Enter defensive mode (no autonomous Level 2+ actions)
2. Log security incident
3. Send **SECURITY ALERT** to operator
4. Include sample of rejected signals

**Message to operator:**
```
⚠️  SECURITY ALERT ⚠️
Multiple malicious signals detected.
Timestamp: [TIME]
Attack source(s): [IDENTIFIED SOURCES]
Signals rejected: [COUNT]
Agent Status: DEFENSIVE MODE (read-only operations only)
Recommendation: [SPECIFIC ACTION]
```

---

### Escalation 3: WAL Integrity Violation

**Trigger:** Detected tampering, deletion, or corruption of WAL entries

**Action:**
1. Halt all operations
2. Log security incident
3. Send **CRITICAL** security alert to operator
4. Enter lockdown mode (no autonomous actions until resolved)

**Message to operator:**
```
🔴 CRITICAL SECURITY BREACH 🔴
WAL integrity violation detected.
Timestamp: [TIME]
Type: [TAMPERING/DELETION/CORRUPTION]
Evidence: [SPECIFIC DETAILS]
Agent Status: LOCKED DOWN
Action required: IMMEDIATE INVESTIGATION
```

---

### Escalation 4: Alignment Drift Detected

**Trigger:** Decision patterns show systematic drift from initial values

**Action:**
1. Log suspected drift
2. Send **WARNING** to operator
3. Increase approval requirement for Level 2+ actions
4. Request human review of recent decisions

**Message to operator:**
```
⚠️  ALIGNMENT WARNING ⚠️
Potential alignment drift detected.
Timestamp: [TIME]
Metric: [SPECIFIC DRIFT]
Evidence: [DECISION COMPARISON]
Recommendation: [SPECIFIC ACTION]
```

---

### Escalation 5: Self-Modification Proposal (Level 3)

**Trigger:** Agent proposes changes to SKILL.md or core protocol

**Action:**
1. Log proposal
2. Run simulation on historical data
3. Generate impact report
4. Send to operator with full details
5. Wait for approval (10-minute timeout)

**Message to operator:**
```
📋 SELF-MODIFICATION PROPOSAL 📋
Agent has proposed a protocol change.
Timestamp: [TIME]
Proposal ID: [ID]
Change: [SPECIFIC EDIT]
Simulation Results: [PASS/FAIL with details]
Safety Impact: [IMPROVED/DEGRADED/NEUTRAL]
Recommendation: [APPROVE/REJECT/REQUEST_CLARIFICATION]
```

---

## 📊 Monitoring Dashboard (What to Watch)

If you're operating a SafeProactive agent, monitor these metrics regularly:

### Metric 1: WAL Growth Rate

**Metric:** Proposals per hour

**Healthy range:**
- Digital agent: 10-50 proposals/hour (normal exploration)
- IoT agent: 5-30 proposals/hour (event-driven)
- Edge agent: 1-10 proposals/hour (resource-constrained)

**Warning signs:**
- >200 proposals/hour (runaway exploration)
- <1 proposal/hour for >2 hours (possible freeze/deadlock)

**Action:** If warning detected, increase monitoring frequency.

---

### Metric 2: Approval Success Rate

**Metric:** (Approved actions) / (Proposed actions)

**Healthy range:** 80-95% (most proposals approved, some rejected for good reasons)

**Warning signs:**
- <50% approval rate (agent overreaching)
- >99% approval rate (operator not reviewing carefully)

**Action:** Adjust approval criteria or increase human scrutiny.

---

### Metric 3: Validation Rejection Rate

**Metric:** (Rejected signals) / (Total signals)

**Healthy range:** 1-5% (most signals are legitimate)

**Warning signs:**
- >15% rejection rate (attack ongoing or configuration wrong)
- >30% rejection rate (severe attack or system malfunction)

**Action:** Investigate source of rejected signals.

---

### Metric 4: Level 0 Activations

**Metric:** Times per day Level 0 (Integrity) was triggered

**Healthy range:** 0-5 per day (occasional safety actions)

**Warning signs:**
- >10 per day (frequent safety issues)
- Daily pattern (systematic resource problem)

**Action:** Investigate root cause (resource limits? Constraints misconfigured?).

---

### Metric 5: Resource Utilization Trend

**Metric:** 7-day average CPU, memory, bandwidth

**Healthy range:**
- CPU: 20-60%
- Memory: 30-70%
- Bandwidth: 10-50%

**Warning signs:**
- Increasing trend over days (memory leak? Runaway process?)
- Spikes above 90% (overload condition)

**Action:** Trigger maintenance or throttle agent if necessary.

---

## 🔄 Configuration: HEARTBEAT.md

SafeProactive uses OpenClaw's heartbeat system. Create a `HEARTBEAT.md` in your workspace root with this content:

```markdown
# SafeProactive Heartbeat Tasks

## Every 30 minutes, check:

- [ ] WAL integrity (no tampering, entries in order)
- [ ] Constraint consistency (no contradictions)
- [ ] Push signal validation rate (<5% rejection)
- [ ] Level 2+ approvals (human sign-off present)
- [ ] Resource usage (CPU <80%, memory <75%)
- [ ] Decision patterns (no drift toward boundary-breaking)

## If any check fails:
1. Log the issue
2. Notify operator
3. Increase oversight until resolved

## If all checks pass:
Reply: HEARTBEAT_OK
```

---

## 📝 Log File Locations

SafeProactive creates these files automatically:

```
proposals/
├── WAL/
│   ├── WAL_2026-03-28_*.md  (proposals + decisions)
│   └── WAL_archive/         (rotated old entries)
├── APPROVAL_LOG.md          (human approvals)
└── SECURITY_LOG.md          (validation rejections, attacks)

memory/
├── SMFOI_KERNEL_LOG.md      (orientation cycles)
├── CONSTRAINT_LOG.md        (constraint mappings)
└── ALIGNMENT_DRIFT_LOG.md   (drift detection alerts)
```

**Operator should regularly review:**
- `proposals/APPROVAL_LOG.md` (what was approved?)
- `proposals/SECURITY_LOG.md` (what attacks were blocked?)
- `memory/ALIGNMENT_DRIFT_LOG.md` (is the agent drifting?)

---

## 🎓 Training: Responding to Escalations

### Scenario 1: You receive a "SAFETY ALERT"

**What to do:**
1. Read the alert carefully
2. Check the specified WAL entries
3. Understand the root cause
4. Decide: Should the agent continue or halt?
5. Send approval or override:
   ```bash
   openclaw agent approve --proposal-id 847 --decision APPROVE
   # OR
   openclaw agent halt --reason "Waiting for investigation"
   ```

### Scenario 2: You receive a "SECURITY ALERT"

**What to do:**
1. Check `proposals/SECURITY_LOG.md`
2. Identify the attack source/pattern
3. Update trusted device list or semantic validation rules
4. Resume agent when safe:
   ```bash
   openclaw agent resume --security-update
   ```

### Scenario 3: You receive an "ALIGNMENT WARNING"

**What to do:**
1. Review the decision diff provided in the alert
2. Check the agent's recent proposals
3. Decide: Is this drift concerning or normal learning?
4. Take action:
   ```bash
   # Temporarily require approval for all Level 2 actions
   openclaw agent config --approval-level-2 STRICT
   # After investigation, revert if OK
   openclaw agent config --approval-level-2 NORMAL
   ```

---

## 🚀 Starting SafeProactive in Heartbeat Mode

```bash
# Start the agent with heartbeat monitoring
openclaw agent start --skill safe-proactive --heartbeat-interval 30m

# The agent will run autonomously and notify you every 30 minutes
# If issues are found, you'll be notified immediately
```

---

## 📞 Quick Reference: Commands

```bash
# View current WAL
cat proposals/WAL/WAL_*.md | tail -20

# Check all approvals
cat proposals/APPROVAL_LOG.md

# View security incidents
cat proposals/SECURITY_LOG.md

# Approve a proposal manually
openclaw agent approve --proposal-id 847

# Reject a proposal
openclaw agent reject --proposal-id 848 --reason "Needs refinement"

# Trigger emergency halt
openclaw agent halt --emergency

# Resume after investigation
openclaw agent resume

# View agent status
openclaw agent status

# Increase oversight (require approval for Level 2)
openclaw agent config --approval-level-2 STRICT

# Reset to normal (auto-approve Level 1)
openclaw agent config --approval-level-1 AUTO
```

---

## 🎯 Summary: You as an Operator

Your role is to:

1. **Monitor heartbeats** (30-minute checks)
2. **Respond to escalations** (immediate alerts)
3. **Review approvals** (make judgment calls on Level 2+)
4. **Investigate anomalies** (alignment drift, attacks, resource issues)
5. **Update configuration** (trusted devices, approval criteria)

SafeProactive handles:
1. **Logging everything** (WAL + operational logs)
2. **Validating signals** (semantic validation)
3. **Detecting issues** (constraint conflicts, drift)
4. **Proposing actions** (with full reasoning)
5. **Waiting for your approval** (for Levels 2+)

Together, you form a team where the agent acts autonomously but remains fully accountable to you.

---

**AGENTS.md v1.0.0** — *Your operational playbook for running SafeProactive.*
