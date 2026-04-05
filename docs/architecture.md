# Architecture Overview

## System Context

The TINA Testbed implements a **planetary-scale distributed intelligence** architecture where multiple AI agents coordinate to monitor Earth systems and generate evolutionary proposals aligned with SPEACE Transition goals.

## Core Components

### 1. Orchestrator
- **Runtime:** OpenClaw agent (DigitalDNA + SMFOI-KERNEL + SafeProactive)
- **Responsibilities:**
  - Distribute data collection tasks to specialized agents
  - Collect and synthesize daily reports
  - Compute SPEACE Alignment Scores for proposals
  - Manage SafeProactive proposal queue
  - Trigger self-evolution cycles (DigitalDNA mutations)

### 2. Specialized Agents (7)
Each agent is an independent OpenClaw sub-agent with:
- **Domain-specific prompt** (see `scientific-team/agents/`)
- **Dedicated data sources** (public APIs)
- **Report template** (JSON/Markdown)
- **SPEACE Alignment scoring logic** (0-100 scale)

Agents operate in parallel and report via filesystem to orchestration hub.

### 3. Data Layer
- **Inputs:** Public APIs (NASA, NOAA, UN, World Bank, WHO, ESA, etc.)
- **Internal storage:** `scientific-team/reports/` (per-agent daily reports)
- **State:** `team_state.json` (iteration, agent status, metrics)

### 4. Output Products
- **Daily Planetary Health Brief** (`daily-brief-YYYY-MM-DD.md`) — synthesized summary
- **SafeProactive Proposals** — autonomous or human-reviewed
- **Archive** — historical reports for trend analysis

### 5. Governance Layer
- **SafeProactive:** All proposals categorized by risk; Medium+ requires human approval
- **DigitalDNA:** Evolutionary engine mutates agent configurations every 13 cycles
- **SMFOI-KERNEL:** Orientation protocol ensures agents maintain SPEACE-aligned goals

## Communication Flow

```
[External APIs] → [Agent Data Fetch] → [Agent Analysis] → [Report File]
                                                  ↓
[Orchestrator Synthesis] → [Daily Brief] → [SPEACE Alignment Scoring] → [SafeProactive]
```

## Deployment Options

1. **Single-node (reference):** All agents on one OpenClaw instance (this repo)
2. **Distributed:** Agents deployed across geographically distributed nodes for resilience
3. **Hybrid:** Core orchestrator centrally, edge agents locally for latency-sensitive domains

## Scalability Considerations

- Adding new domains: create new agent profile and register in orchestrator
- Data source rate limits: implement caching and scheduling
- High availability: replicate orchestrator state to backup node
- Future: peer-to-peer agent communication via libp2p for autonomous coordination

## Security & Ethics

- All data sources are public; no personal data processed
- Proposals with geopolitical impact require human review
- DigitalDNA mutations must preserve core SPEACE values (Earth Charter, SDGs)
- Blockchain integration only for proposal auditing, not for autonomous execution

## Evolution Roadmap

- **Phase 1 (current):** Manual report generation, human synthesis
- **Phase 2:** Automated daily brief, integrated alerting
- **Phase 3:** Cross-agent learning (agents share insights autonomously)
- **Phase 4:** Global deployment with satellite nodes
- **Phase 5:** Full autonomy with human oversight via SafeProactive
