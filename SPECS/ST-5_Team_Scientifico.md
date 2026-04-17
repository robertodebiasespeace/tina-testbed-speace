# SCHEDA TECNICA ST-5 – SPEACE Team Scientifico AI Multidisciplinare
**Versione:** 1.0  
**Data:** 17 aprile 2026  
**Stato:** Operativo

---

## 1. Descrizione

Team di agenti specializzati + Orchestrator gestito da SPEACE Cortex. Realizza la "direzione scientifica internazionale multidisciplinare" richiesta dal Rigene Project.

## 2. Struttura Team

```
Team_Scientifico/
├── orchestrator/
│   └── orchestrator.py
├── agents/
│   ├── climate_ecosystems_agent.py
│   ├── economics_resource_agent.py
│   ├── governance_ethics_agent.py
│   ├── technology_integration_agent.py
│   ├── health_pandemic_agent.py
│   ├── social_cohesion_agent.py
│   ├── space_extraterrestrial_agent.py
│   ├── adversarial_agent.py          # ← NUOVO (proposto)
│   └── evidence_verification_agent.py # ← NUOVO (proposto)
├── output/
│   ├── daily_briefs/
│   ├── early_warnings/
│   ├── evolutionary_proposals/
│   └── regulatory_briefs/            # ← NUOVO
└── shared/
    └── team_state.json
```

## 3. Agenti Attivi (7 + Orchestrator)

| Agente | Focus | Output |
|--------|-------|--------|
| **Orchestrator** | Coordinamento team, aggregazione output | Daily Planetary Health Brief |
| **Climate & Ecosystems Agent** | Crisi climatica, ecosistemi, ambiente | Report emissioni, previsioni |
| **Economics & Resource Agent** | Economia circolare, risorse globali | Analisi risorse, trend economici |
| **Governance & Ethics Agent** | Governance, etica, compliance | Framework etici, raccomandazioni |
| **Technology Integration Agent (TFT)** | Tech 4.0, integrazione sistemi | Technology Synergy Map |
| **Health & Pandemic Agent** | Sanità, pandemie, salute globale | Early Warning System |
| **Social Cohesion Agent** | Coesione sociale, UN SDG | Analisi sociali, indicatori |
| **Space & Extraterrestrial Agent** | Spazio, espansione extraterrestre | Roadmap spaziale |

## 4. Agenti Proposti (Estensione)

| Agente | Ruolo | Priorità | Focus |
|--------|-------|----------|-------|
| **Adversarial Agent (Critic)** | Criticare proposte, evidenziare bias, rischi nascosti | ALTA | Risk mitigation |
| **Evidence Verification Agent** | Fact-checking, cross-check dati, affidabilità fonti | ALTA | Quality assurance |
| **Regulatory & Compliance Monitor** | EU AI Act, NIST, ISO 42001, Singapore Framework | ALTA | Compliance |

## 5. Orchestrator – Specifiche

```yaml
orchestrator:
  role: "Coordina i 7+ agenti specialisti"
  
  workflow:
    1. Distribute task to all agents
    2. Collect partial outputs
    3. Aggregate and synthesize
    4. Generate unified brief
    5. Queue proposals for SafeProactive
  
  scheduling:
    daily_brief: "00:00 UTC"
    early_warning: "on_trigger"
    proposal_review: "every_60_minutes"
  
  output_format:
    daily_brief: "markdown"
    early_warning: "json"
    proposal: "SafeProactive markdown"
```

## 6. Output Principali

### 6.1 Daily Planetary Health Brief

```yaml
daily_planetary_health_brief:
  generated: "daily at 00:00 UTC"
  sections:
    - climate_status: "Emissioni, temperature, previsioni"
    - ecosystem_health: "Biodiversity, deforestation, ocean health"
    - economic_indicators: "Resource usage, circular economy metrics"
    - technology_integration: "AI advancement, IoT deployment, quantum"
    - health_pandemics: "Disease outbreaks, healthcare access"
    - social_cohesion: "UN SDG progress, inequality metrics"
    - governance_ethics: "Policy changes, ethical framework updates"
    - space_status: "Space exploration, satellite data"
    - regulatory_updates: "EU AI Act, NIST, ISO changes"
    - speace_recommendations: "Proposed mutations, actions"
  
  distribution:
    - WhatsApp (Roberto De Biase)
    - Email
    - File: "Team_Scientifico/output/daily_briefs/YYYY-MM-DD.md"
```

### 6.2 Early Warning System

```yaml
early_warning_system:
  triggers:
    - climate_anomaly: "temp_change > 2C from baseline"
    - pandemic_risk: "new_outbreak_detected"
    - economic_crisis: "market_volatility > 20%"
    - social_unrest: "protest_aggregation_detected"
    - technology_risk: "AI_safety_incident"
  
  alert_levels:
    - info: "Monitor, log"
    - watch: "Human notification"
    - warning: "Human + Team review"
    - critical: "Immediate action + all stakeholders"
  
  output_format: "JSON"
```

### 6.3 Evolutionary Proposals

```yaml
evolutionary_proposals:
  format: "SafeProactive PROPOSALS.md"
  risk_levels: ["low", "medium", "high"]
  approval_flow: "SafeProactive standard"
  examples:
    - "Increase yield_priority by 2"
    - "Add new sensor integration (NOAA)"
    - "Update alignment weights"
```

### 6.4 Global Regulatory Brief ← NUOVO

```yaml
regulatory_brief:
  frequency: "daily"
  sources:
    - EU_AI_Act: "artificialintelligenceact.eu"
    - NIST: "NIST AI RMF"
    - ISO_42001: "ISO AI Management"
    - OECD: "OECD AI Policy Observatory"
    - Singapore: "Model AI Governance Framework"
  
  sections:
    - new_regulations: "Summary of new rules"
    - compliance_impact: "Impact on SPEACE"
    - required_actions: "What SPEACE must do"
    - risk_assessment: "Compliance risk level"
  
  integrated_into: "Daily Planetary Health Brief"
```

## 7. Interazione con SPEACE Cortex

```
SPEACE Cortex
      │
      │ 1. Invio task (es. "Genera Daily Brief")
      ▼
┌─────────────────────────────────────┐
│         Team Scientifico             │
│  ┌─────────────────────────────┐    │
│  │    Orchestrator             │    │
│  └──────────────┬──────────────┘    │
│                 │                   │
│    ┌────────────┼────────────┐      │
│    ▼            ▼            ▼      │
│ [Agent 1]  [Agent 2]  ... [Agent N] │
│  Climate   Economics           Space │
│    └────────────┼────────────┘      │
│                 │                   │
│                 ▼                   │
│         [Aggregated Output]         │
└─────────────────────────────────────┘
      │
      │ 2. Ricevi output + proposals
      ▼
SafeProactive → Proposal review → Execution
```

## 8. Interazione Multi-Framework

```
SPEACE Cortex (OpenClaw - Port 8000)
      │
      │ REST API
      ▼
SuperAGI (Port 8002 - Workflow Engine)
      │
      │ Orchestrates
      ▼
┌─────────────────────────────────────────────┐
│     Team Scientifico Workflow (SuperAGI)    │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐       │
│  │Climate  │ │Economics│ │Health   │ ...   │
│  │Agent    │ │Agent    │ │Agent    │       │
│  └────┬────┘ └────┬────┘ └────┬────┘       │
│       └──────────┼──────────┘             │
│                  ▼                         │
│           [Orchestrator]                   │
│                  │                         │
│                  ▼                         │
│         [Daily Brief Output]               │
└─────────────────────────────────────────────┘
      │
      │ World Model sync
      ▼
AnythingLLM (Port 8003 - RAG/Knowledge)
```

## 9. Metriche Team

| Metrica | Valore |
|---------|--------|
| Agenti attivi | 7 + Orchestrator |
| Daily briefs generati | 12+ |
| Proposals in coda | 28 |
| Proposals executati | ~24 |
| Alignment Score | 67.3/100 |
| Next heartbeat | 60 min |

## 10. Prossimi Passi

| Step | Azione | Priorità |
|------|--------|----------|
| 1 | Aggiungere Adversarial Agent | ALTA |
| 2 | Aggiungere Evidence Verification Agent | ALTA |
| 3 | Integrare Regulatory Monitor Agent | ALTA |
| 4 | Passare orchestrazione a SuperAGI | MEDIA |
| 5 | Implementare Real-time data feeds | MEDIA |

---

## 11. Riferimenti

- **TINA Framework (G20):** https://www.academia.edu/165241120/TINA_Framework_G20_Combined_EN
- **Rigene Project:** https://www.rigeneproject.org
- **UN SDG:** https://sdgs.un.org/goals
