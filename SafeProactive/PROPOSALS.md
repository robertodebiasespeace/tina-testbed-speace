# SafeProactive Proposals Registry

## Proposal Template
```
## Proposal #[ID]
**Date:** [YYYY-MM-DD]
**Author:** SPEACE Cortex / [Agent]
**Risk Level:** [Low/Medium/High/Regulatory]
**SPEACE Alignment Score (pre):** [0-100]
**SPEACE Alignment Score (post est.):** [0-100]
**DigitalDNA Impact:** [Minimal/Moderate/Significant]
**Fitness Function Impact:** [Positive/Negative/Neutral]

### Description
[What the proposal does]

### Risk Assessment
[Analysis of risks]

### Required Approvals
[Who must approve]

### Implementation Plan
[Steps to implement]

---
```

---

## Proposal #001 - Agente Organismico (ST-6) Foundation
**Date:** 2026-04-17
**Author:** SPEACE Cortex
**Risk Level:** High
**SPEACE Alignment Score (pre):** 67.3
**SPEACE Alignment Score (post est.):** 72.0
**DigitalDNA Impact:** Moderate
**Fitness Function Impact:** Positive

### Description
Implementazione base dell'Agente Organismico (ST-6) per espansione sensing multi-modale. Questa proposta getta le fondamenta per l'interconnessione IoT e la mobilità organismica di SPEACE.

### Motivation
- Avanzamento verso Fase 2 (Autonomia Operativa)
- Abilitazione sensing planetario multi-modale
- Preparazione infrastruttura per robotica/IoT fisico
- Allineamento con obiettivi Rigene Project

### Components to Implement

#### 1. IoT Interface Layer
```
speace_organism/
├── iot_interface.py      # Protocollo REST/WebSocket per IoT
├── sensor_protocols/     # Visivo, Acustico, Termico, etc.
└── device_discovery.py   # Auto-discovery sensori
```

#### 2. SMFOI-KERNEL Extension (Organism Mode)
- Step 3 esteso: Push Detection include segnali IoT
- Step 4 esteso: Survival Stack Lv4 per interazione materiale
- Step 5 esteso: Output include attuatori

#### 3. Basic Sensor Simulation
- Dummy sensor data per testing
- Pipeline visivo (camera sim), acustico, termico

### Risk Assessment
| Risk | Level | Mitigation |
|------|-------|------------|
| IoT Security | High | IronClaw sandbox, firewall rules |
| Resource Overload | Medium | RAM budget check, throttling |
| Uncontrolled Actuators | High | Human approval for physical actions |
| Data Privacy | Medium | Encryption, pii handling |

### DigitalDNA Impact
- Nuovo comparto: "Organism Interface" (10° comparto futuro)
- Epigenome: `organism_enabled: true`
- vincoli_fondamentali: `physical_action_requires_approval: true`

### Required Approvals
- Roberto De Biase (human + legal review)

### Implementation Phases
1. **Phase 1:** IoT Interface base (1-2 days)
2. **Phase 2:** Sensor simulation (2-3 days)
3. **Phase 3:** SMFOI extension (2-3 days)
4. **Phase 4:** Integration test (1 day)

### Expected Outcomes
- SPEACE Alignment Score +4.7 (67.3 → 72.0)
- Fitness Function +0.05
- Path toward Fase 2 accelerated
- Foundation for physical agent

---

## Proposal #002 - AnythingLLM World Model Prototipo
**Date:** 2026-04-17
**Author:** SPEACE Cortex
**Risk Level:** Medium
**SPEACE Alignment Score (pre):** 67.3
**SPEACE Alignment Score (post est.):** 70.0
**DigitalDNA Impact:** Moderate
**Fitness Function Impact:** Positive

### Description
Implementazione prototipo di AnythingLLM come World Model / Knowledge Graph per SPEACE. Questo consentirà a SPEACE di mantenere un modello interno della realtà, inferenza, simulazione e cross-framework knowledge sync.

### Motivation
- Completamento Phase 1 del Piano Implementazione (Week 1)
- Abilitazione World Model / Knowledge Graph (9° comparto Cortex)
- Preparazione per SuperAGI orchestration
- Foundation per multi-framework data exchange

### Components to Implement

#### 1. AnythingLLM Installation & Configuration
- Docker container deployment (port 8003)
- Vector database setup (LanceDB embedded)
- Workspace configuration for SPEACE docs

#### 2. Document Ingestion Pipeline
```
ingest/
├── engineering_documents/
├── specs/
├── digitaldna/
└── team_output/
```

#### 3. Query Interface (OpenClaw → AnythingLLM)
- REST endpoint: POST /query
- Request format: JSON with question/context
- Response format: JSON with answer + sources

#### 4. World Model Sync Protocol
- Periodic sync with DigitalDNA updates
- Cross-framework knowledge sharing
- Long-term memory integration

### Risk Assessment
| Risk | Level | Mitigation |
|------|-------|------------|
| Resource Usage | Medium | RAM budget 2.5GB |
| Data Privacy | Low | Local vector store |
| Performance | Low | Embedded DB |

### DigitalDNA Impact
- Epigenome: `world_model_enabled: true`
- New workflow: `world_model_query` integrated in SMFOI
- Comparto 9 (World Model) now functional

### Required Approvals
- Roberto De Biase (Human-in-loop per Medium risk)

### Implementation Phases
1. **Phase 1:** Docker setup + AnythingLLM install (1 day)
2. **Phase 2:** Document ingestion (2 days)
3. **Phase 3:** Query interface development (2 days)
4. **Phase 4:** Integration test with SPEACE Cortex (1 day)

### Expected Outcomes
- SPEACE Alignment Score +2.7 (67.3 → 70.0)
- World Model functional with SPEACE documentation
- Foundation for multi-framework orchestration
- Query response time <2 seconds target
