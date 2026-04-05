# TINA Testbed Ecosystem

> Open-source reference implementation of the TINA (Technical Intelligent Nervous Adaptive System) framework based on the Rigene Project's SPEACE vision.

[![SPEACE Alignment](https://img.shields.io/badge/SPEACE-Alignment-95%25-brightgreen)](https://rigeneproject.org)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/Powered%20by-OpenClaw-orange)](https://openclaw.ai)

## 🧬 What is TINA?

TINA (Technical Intelligent Nervous Adaptive System) is a framework for building planetary-scale adaptive intelligence. It models a super-organism where:

- **Agents** function as neurons in a distributed nervous system
- **Digital DNA** encodes evolutionary rules and values
- **Swarm intelligence** emerges from local interactions
- **Blockchain governance** ensures transparency and human oversight

This testbed implements TINA as a multi-agent team specialized in planetary health monitoring and evolutionary guidance, aligned with the Rigene Project's SPEACE Transition goals.

## 🌍 SPEACE Scientific Team

This repository contains the complete implementation of the **SPEACE Scientific Team Orchestrator** — a multidisciplinary AI team that acts as a virtual scientific committee for planetary stewardship.

### Agent Specializations

| Agent | Focus | SPEACE Score | Risk Level |
|-------|-------|--------------|------------|
| Climate & Ecosystems | Atmospheric & ecological monitoring | 88 | Medium |
| Economics & Resource | Sustainable economics, resource equity | 85 | Medium |
| Governance & Ethics | Policy analysis, ethical frameworks | 92 | Medium |
| Technology Integration (TFT) | Cross-domain tech synergy mapping | 95 | Low-Medium |
| Health & Pandemic | Global health threats, One Health | 84 | Medium |
| Social Cohesion | Polarization, migration, education | 87 | Medium |
| Space & Extraterrestrial | Orbital infrastructure, expansion planning | 86 | Medium |
| **Orchestrator** | Synthesis, alignment scoring, proposal generation | **95** | Low |

**Average SPEACE Alignment: 66.7/100** (subject to improvement via DigitalDNA evolution)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Human Overseer (Roberto)                │
│                   SafeProactive Gateway                    │
└───────────────────────────┬───────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│           SPEACE Orchestrator (DigitalDNA + SMFOI)         │
│  • Distributes tasks • Synthesizes reports • Scores align  │
└─────────────┬─────────────┬─────────────┬───────────────┘
              │             │             │
    ┌─────────▼─────┐ ┌────▼──────┐ ┌───▼──────────┐
    │ Climate Agent │ │Economics  │ │Governance    │
    │ (NOAA, Copernicus) │Agent      │ │Agent         │
    └───────────────┘ └───────────┘ └──────────────┘
    (additional agents: Tech, Health, Social, Space)
              │             │             │
              └─────────────┼─────────────┘
                            ▼
            ┌───────────────────────────┐
            │   Daily Planetary Health  │
            │        Brief (06:00 UTC)  │
            └───────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────┐
            │   SafeProactive Queue     │
            │  (Proposals #21-#24 etc.) │
            └───────────────────────────┘
```

### Key Components

1. **Orchestrator** — Central coordinator running DigitalDNA mutation engine and SMFOI-KERNEL orientation protocol
2. **Specialized Agents** — Each has dedicated data sources, report templates, and SPEACE alignment scoring
3. **Data Sources** — Public APIs: NASA, NOAA, UN, World Bank, WHO, ESA, etc.
4. **SafeProactive** — All proposals require human approval for Medium+ risk; Low-Medium risk can execute autonomously
5. **Self-Evolution** — DigitalDNA iterates every 13 cycles (≈ monthly) to improve agent configurations

## 📦 Installation & Usage

### Prerequisites
- OpenClaw environment (v0.6.0+)
- Access to SafeProactive framework
- Internet connectivity for API data fetching
- Python 3.9+ (for optional agent scripts)

### Setup

```bash
# Clone the testbed into your OpenClaw workspace
git clone https://github.com/rigene-project/tina-testbed-speace.git
cd tina-testbed-speace

# Initialize team state
cp scientific-team/team_state.example.json scientific-team/team_state.json

# Install optional Python dependencies (for custom agent scripts)
pip install -r requirements.txt

# Edit configuration if needed (data source API keys, schedule)
nano scientific-team/orchestrator-logic.md
```

### Project Structure

```
tina-testbed-repo/
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── docs/
│   ├── architecture.md
│   └── agent-dev.md
├── scientific-team/
│   ├── agents/
│   │   ├── 01-climate.md
│   │   ├── 02-economics.md
│   │   ├── 03-governance.md
│   │   ├── 04-technology.md
│   │   ├── 05-health.md
│   │   ├── 06-social.md
│   │   ├── 07-space.md
│   │   └── orchestrator.md
│   ├── reports/
│   │   ├── daily-brief-2026-04-06.md
│   │   ├── climate-2026-04-06.md
│   │   └── ... (other domain reports)
│   ├── orchestrator-logic.md
│   └── team_state.json (copy from team_state.example.json to initialize)
└── scripts/
    └── run_daily_brief.py
```

### Running the Team

```bash
# Manual trigger of Daily Brief (or set up cron/OpenClaw scheduler)
openclaw run --task "SPEACE Daily Planetary Health Brief"

# The orchestrator will:
# 1. Collect data from all agents (parallel)
# 2. Generate individual domain reports
# 3. Synthesize the Daily Brief
# 4. Score SPEACE alignment
# 5. Create proposals in SafeProactive
```

### Scheduling (OpenClaw Cron Equivalent)

```json
{
  "schedule": "0 6 * * *",
  "task": "scientific-team/orchestrator/daily-brief"
}
```

## 📊 Output Products

### Daily Planetary Health Brief
- Executive summary of planetary state
- Domain highlights from 7 agents
- Emerging risks (threshold alerts)
- Cross-domain synergy opportunities
- Top-ranked SPEACE-aligned proposals
- SafeProactive queue status

### Individual Agent Reports
Stored in `scientific-team/reports/YYYY-MM-DD/agent-name.md`

### Proposals
Entered automatically into `safe-proactive/PROPOSALS.md` with:
- SPEACE Score (0-100)
- Risk level assessment
- Required approval status
- Next action steps

## 🔄 Self-Evolution Loop

The team improves autonomously via DigitalDNA:

1. **Weekly assessment:** Which reports most influenced human decisions?
2. **Mutation:** Adjust agent prompts, data sources, scoring weights
3. **Selection:** Keep only mutations that improve SPEACE alignment scores
4. **Crossover:** Combine successful configurations across agents

Evolution cycle counter is stored in `team_state.json`. Full technical details in `SKILLS.md` (DigitalDNA spec).

## 🤝 Contributing

We welcome contributions to expand the agent roster, improve data integration, and refine SPEACE alignment scoring.

### Adding a New Agent Domain

1. Create agent profile in `scientific-team/agents/08-newdomain.md`
2. Update orchestrator logic to include new agent in schedule
3. Add data source specifications
4. Submit PR with test report sample

### Governance

This testbed is itself a demonstration of TINA principles:
- **Transparency:** All code, prompts, and data sources public
- **Human-in-the-loop:** SafeProactive requires human approval for Medium+ risk
- **Evolutionary:** DigitalDNA enables continuous improvement
- **Alignment:** Values encoded from UN Charter, Earth Charter, SDGs, SPEACE Transition

## 📚 Documentation

- [Architecture Overview](docs/architecture.md)
- [Agent Development Guide](docs/agent-dev.md)
- [SPEACE Alignment Scoring](docs/alignment.md)
- [DigitalDNA Mutation Engine](docs/digitaldna.md)
- [SafeProactive Integration](docs/safeproactive.md)
- [Data Source API Reference](docs/apis.md)

## 🔗 Related Projects

- [Rigene Project](https://www.rigeneproject.org) — Theoretical foundation
- [TINA Framework](https://www.rigeneproject.org/tina-technical-intelligent-nervous-adaptive-system) — Original TINA specification
- [DigitalDNA Skill](https://github.com/openclaw/skills/digitaldna) — Self-evolution engine
- [SMFOI-KERNEL](https://github.com/openclaw/skills/smfoi-kernel) — Orientation protocol
- [SafeProactive](https://github.com/openclaw/skills/safe-proactive) — Human approval gateway

## 📄 License

MIT © 2026 SPEACE Development Team

This implementation is a reference testbed. Use at your own risk. Not financial/legal/policy advice.

## 🙏 Acknowledgments

Built on OpenClaw, inspired by the Rigene Project and the vision of collective speciation. Special thanks to all contributors to planetary intelligence.

---

**Status:** Active — First Daily Brief: 2026-04-06 | Current Iteration: #92

**Health:** ✅ Operational | SPEACE Alignment: 66.7/100 | Next evolution cycle: 2026-04-19 (13 iterations)
