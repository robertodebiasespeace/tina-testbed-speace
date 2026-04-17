# Multi-Framework Architecture
**Versione:** 1.0
**Data:** 17 aprile 2026
**Stato:** Design - Ready for Implementation

---

## 1. Framework Roles

### OpenClaw (SPEACE Cortex Principal)
- **Port:** 8000
- **RAM Allocation:** 4.5 GB
- **Focus:** Skill marketplace, Claude Code integration
- **Responsibilities:**
  - Main SPEACE Cortex orchestrator
  - Decision making hub
  - SMFOI-KERNEL host
  - DigitalDNA management
  - SafeProactive integration

### IronClaw (Secure Execution)
- **Port:** 8001
- **RAM Allocation:** 2.5 GB
- **Focus:** Security, sandboxing, WASM
- **Responsibilities:**
  - Critical operations isolation
  - Wallet/transactions execution
  - Sandboxed code evaluation
  - Compliance enforcement

### SuperAGI (Orchestration)
- **Port:** 8002
- **RAM Allocation:** 3.0 GB
- **Focus:** Multi-agent workflow engine
- **Responsibilities:**
  - Team Scientifico orchestration
  - Agent coordination
  - Workflow automation
  - Task distribution

### AnythingLLM (World Model / Knowledge Graph)
- **Port:** 8003
- **RAM Allocation:** 2.5 GB
- **Focus:** RAG, Knowledge management
- **Responsibilities:**
  - World Model maintenance
  - Knowledge base (ingest SPEACE docs)
  - Context retrieval
  - Long-term memory

### NanoClaw (Future Edge/IoT)
- **Port:** 8004
- **RAM Allocation:** 1.5 GB
- **Focus:** Edge, lightweight, IoT
- **Responsibilities:**
  - Sensor data collection
  - Edge processing
  - IoT device management
  - Climate/data feeds

---

## 2. Communication Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SPEACE CORTEX (OpenClaw)                     │
│                   Port 8000 · REST + Redis                      │
└─────────────────────────────────────────────────────────────────┘
                              │
           ┌──────────────────┼──────────────────┐
           │                  │                  │
           ▼                  ▼                  ▼
    ┌────────────┐    ┌────────────┐    ┌────────────┐
    │ IronClaw   │    │  SuperAGI  │    │ AnythingLLM │
    │ Port 8001  │    │  Port 8002 │    │  Port 8003 │
    │ Sandbox    │    │  Workflow  │    │ World Model│
    │ (Rust/WASM)│    │  Engine    │    │  (RAG)     │
    └────────────┘    └────────────┘    └────────────┘
           │                  │                  │
           └──────────────────┼──────────────────┘
                              │
                     ┌─────────────────┐
                     │ Redis Pub/Sub   │
                     │ localhost:6379  │
                     │ (Message Broker)│
                     └─────────────────┘
                              │
                     ┌─────────────────┐
                     │ Shared Volume   │
                     │ /srv/speace/   │
                     │ shared/         │
                     └─────────────────┘
           ┌────────────┐
           │ NanoClaw   │
           │ Port 8004  │
           │ Edge/IoT   │
           └────────────┘
```

---

## 3. Communication Protocols

### 3.1 REST API Endpoints

```yaml
endpoints:
  openclaw:
    - GET  /status              # Cortex status
    - POST /task                # Submit task
    - POST /mutation            # DigitalDNA mutation
    - GET  /proposals          # SafeProactive proposals

  ironclaw:
    - POST /execute_sandboxed   # Execute in sandbox
    - POST /validate_operation  # Security validation
    - GET  /sandbox_status      # Sandbox health

  superagi:
    - POST /workflow/start      # Start workflow
    - POST /workflow/stop      # Stop workflow
    - GET  /agents/status       # Agent status list
    - POST /task/distribute    # Distribute task to agents

  anythingllm:
    - POST /query               # Query World Model
    - POST /ingest              # Ingest new documents
    - GET  /knowledge/graph     # Get knowledge graph
    - POST /sync                # Sync with other frameworks
```

### 3.2 Redis Pub/Sub Channels

```yaml
channels:
  speace.cortex.broadcast:     # Main cortex broadcast
  speace.ironclaw.events:       # Security events
  speace.superagi.workflow:     # Workflow updates
  speace.anythingllm.updates:   # Knowledge updates
  speace.nanoclaw.sensors:      # Sensor data streams
  speace.team.analysis:         # Team scientifico analysis
```

### 3.3 Message Format

```json
{
  "sender": "openclaw|ironclaw|superagi|anythingllm|nanoclaw",
  "receiver": "framework_name|multicast|broadcast",
  "task_type": "query|execute|workflow|sync|alert",
  "payload": {
    "data": {},
    "metadata": {}
  },
  "timestamp": "2026-04-17T18:00:00Z",
  "correlation_id": "uuid-v4",
  "reply_to": "optional-channel"
}
```

---

## 4. Shared Volume Structure

```
/srv/speace/
├── shared/
│   ├── team_state.json         # Team Scientifico state
│   ├── PROPOSALS.md            # SafeProactive proposals
│   ├── world_model/
│   │   ├── embeddings/         # Vector embeddings
│   │   └── graph.json          # Knowledge graph
│   ├── cortex/
│   │   ├── genome.yaml
│   │   ├── epigenome.yaml
│   │   └── snapshots/
│   └── logs/
│       ├── smfoi_kernel.log
│       ├── safe_proactive.log
│       └── team_scientifico.log
├── openclaw/
├── ironclaw/
├── superagi/
├── anythingllm/
└── nanoclaw/
```

---

## 5. Security Model

```yaml
security:
  network:
    localhost_only: true
    firewall_rules: active
    allowed_ports: [8000, 8001, 8002, 8003, 8004, 6379]

  authentication:
    internal_mtls: optional (production)
    api_keys_for_external: required

  data_protection:
    encryption_at_rest: true
    encryption_in_transit: true
    pii_handling: strict
```

---

## 6. Implementation Phases

### Phase 1: Core Setup (Week 1)
- [x] Create directory structure
- [ ] Deploy IronClaw container (Docker)
- [ ] Integrate AnythingLLM as World Model
- [ ] Create OpenClaw → AnythingLLM query endpoint
- [ ] Test rollback: trigger low-risk DigitalDNA mutation

### Phase 2: Team Integration (Week 2)
- [ ] Add NanoClaw edge agent: fetch NOAA climate data
- [ ] SuperAGI workflow: orchestrate 3 agents
- [ ] Validate SPEACE Alignment scoring

### Phase 3: Advanced Features
- [ ] Full multi-framework orchestration
- [ ] Swarm scaling (target 50+ agents)
- [ ] Advanced RAG and knowledge synthesis

---

## 7. RAM Budget Summary

| Framework | RAM | Notes |
|-----------|-----|-------|
| OpenClaw | 4.5 GB | Maximum |
| IronClaw | 2.5 GB | Critical ops |
| SuperAGI | 3.0 GB | Team orchestration |
| AnythingLLM | 2.5 GB | Knowledge + RAG |
| **Total** | 12.5 GB | OK (3.5GB OS margin) |

---

**Documento:** Multi-Framework Architecture v1.0
**Creato:** 17 aprile 2026
**Stato:** Design completo, pronto per implementazione
