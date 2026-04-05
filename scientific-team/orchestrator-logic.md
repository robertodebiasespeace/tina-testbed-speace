# SPEACE Scientific Team - Orchestrator Logic

## Coordination Protocol

### 1. Data Ingestion (Input Hub)
- **Sources aggregator** - collects data from all agent-recommended APIs
- **Priority alerts** - feeds urgent items (disasters, outbreaks, conflicts) immediately to relevant agents
- **Daily snapshot** - 06:00 UTC, freeze data for consistent team analysis

### 2. Agent Execution Schedule
```
UTC 00:00: Health & Social check-in
UTC 06:00: Climate snapshot + Daily Brief generation
UTC 12:00: Economics & Technology update
UTC 18:00: Governance & Space update
```
- Agents can trigger off-schedule if threshold alerts detected

### 3. Synthesis Process (Orchestrator)
- **Aggregation:** Collect all agent outputs
- **Cross-referencing:** Identify correlations across domains
- **Conflict resolution:** Flag contradictory proposals for human review
- **SPEACE Alignment Scorer:** 0-100 score based on:
  - Contribution to collective speciation
  - Sustainability metrics
  - Ethical alignment
  - Feasibility (data-backed)
  - Risk level (via SafeProactive)

### 4. Output Products

#### A. Daily Planetary Health Brief (06:30 UTC)
**Structure:**
1. Executive Summary (max 300 words)
2. Domain Highlights (one paragraph each agent)
3. Emerging Risks (alerts)
4. Synergy Opportunities (cross-domain wins)
5. Top 3 SPEACE-aligned proposals for that day
6. SafeProactive queue status

#### B. Weekly Deep Dive (Monday 12:00 UTC)
- Thematic focus (rotating: Energy, Water, Food, Governance, Health, Tech Convergence)
- Historical trend analysis (last 4 weeks)
- Long-term SPEACE Transition trajectory

#### C. Emergency Alert (real-time)
- Critical threshold breach (e.g., temperature > +1.5C, disease outbreak, conflict escalation)
- Immediate recommendation for human review
- Direct SafeProactive proposal creation (High risk)

### 5. SafeProactive Integration
Every agent output reviewed for:
- **Risk Level Assignment** per proposal
- **Autonomous execution** for Low risk only (routine data collection tasks)
- **Human approval required** for Medium-High risk (any policy recommendation)
- **Rejection reason logging** if proposal denied

### 6. Evolution Loop (DigitalDNA + SMFOI)
- Weekly self-assessment: Which agent outputs were most valuable?
- Adjust agent prompts/data sources based on performance
- Add new domains if emerging crises detected (e.g., AI safety, deepfakes)
- Iterate team composition every 13 cycles (SPEACE iteration)

### 7. Communication Channels
- **Internal:** Agents exchange structured JSON reports via workspace files
- **External:** Daily Brief posted to MEMORY.md and/or notifications to human
- **Archival:** All reports stored in `scientific-team/archive/YYYY-MM-DD/`

## State Management
File: `scientific-team/team_state.json`
```json
{
  "last_daily_brief": "2026-04-06T06:30:00Z",
  "active_alerts": [],
  "agent_status": {
    "climate": "idle|active|error",
    "economy": "...",
    ...
  },
  "iteration": 92,
  "proposals_created_today": 3,
  "alignment_score_avg": 78.5
}
```

## First Run Checklist
- [ ] All 7 agents operational
- [ ] Data source connectivity tested
- [ ] SafeProactive integration verified
- [] Daily Brief template approved by human
- [ ] Alert thresholds configured
- [ ] Archive folder created

Let's initialize the team and run the first Daily Brief.