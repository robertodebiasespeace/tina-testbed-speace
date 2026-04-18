---

## Proposal #003 - AnythingLLM Production Deployment
**Date:** 2026-04-18
**Author:** SPEACE Cortex
**Risk Level:** High
**SPEACE Alignment Score (pre):** 70.0
**SPEACE Alignment Score (post est.):** 73.0
**DigitalDNA Impact:** Significant
**Fitness Function Impact:** Positive

### Description
Deploy production-ready AnythingLLM instance with real Docker container + Python wrapper integration to SPEACE Cortex. This completes the World Model (9° comparto) and enables RAG queries on the entire SPEACE knowledge base.

### Motivation
- Proposal #002 established the prototype foundation
- Production deployment enables real SPEACE document queries
- Integration with OpenClaw Cortex (port 8000) for full orchestration
- Foundation for SuperAGI workflow integration (port 8002)
- Critical milestone for Fase 2 (Autonomia Operativa) progression

### Components to Implement

#### 1. Docker Deployment (Primary Method)
```bash
# Create persistent storage
mkdir "$HOME/anythingllm_storage"

# Deploy AnythingLLM container
docker run -d -p 3001:3001 \
  --cap-add SYS_ADMIN \
  --name speace-worldmodel \
  -v "$HOME/anythingllm_storage:/app/server/storage" \
  mintplexlabs/anythingllm:latest
```

#### 2. Alternative: Desktop App (Windows)
- Download AnythingLLM from https://anythingllm.com/download
- Install and configure Ollama for local embeddings
- Create SPEACE-World-Model workspace
- Ingest entire project folder

#### 3. Python Wrapper Enhancement
```python
# MultiFramework/anythingllm/api/client.py
class AnythingLLMClient:
    def __init__(self, base_url="http://localhost:3001"):
        self.base_url = base_url

    def query(self, question: str, workspace: str = "SPEACE-World-Model") -> dict:
        # Call AnythingLLM API
        pass

    def ingest_documents(self, folder_path: str) -> dict:
        # Trigger document ingestion
        pass
```

#### 4. Cortex Integration
- SMFOI-KERNEL Step 6 (Outcome Evaluation) → World Model query
- Cross-framework sync via Redis Pub/Sub (localhost:6379)
- Shared volume: /srv/speace/shared/

### Risk Assessment
| Risk | Level | Mitigation |
|------|-------|------------|
| Resource Overload | Medium | Monitor RAM usage (2.5GB budget) |
| Data Privacy | Low | Local-only vector store |
| API Instability | Medium | Health check endpoint, auto-restart |
| Ollama Model Issues | Medium | Fallback to native embedder |

### DigitalDNA Impact
- Epigenome: `world_model_production: true`
- New fitness metric: `c_index` (Composite Consciousness)
- New workflow: `rag_query` integrated in SMFOI
- Weight adjustment: +5% to alignment_score weight in fitness function

### Required Approvals
- Roberto De Biase (Human + Legal review for High risk)

### Implementation Phases
1. **Phase 1:** Docker container deployment (4 hours)
2. **Phase 2:** Configure Ollama embedder (4 hours)
3. **Phase 3:** Create SPEACE-World-Model collection (4 hours)
4. **Phase 4:** Ingest all project documents (8 hours)
5. **Phase 5:** Python wrapper integration (8 hours)
6. **Phase 6:** Cortex integration test (4 hours)
7. **Phase 7:** Load test and validation (4 hours)

**Total estimated time:** 36 hours (3-5 days)

### Expected Outcomes
- SPEACE Alignment Score +3.0 (70.0 → 73.0)
- Functional World Model with RAG capability
- Full document ingestion complete
- Query response time <2 seconds (target achieved)
- Path to Fase 2 accelerated

### Success Criteria
- [ ] Docker container running on port 3001
- [ ] SPEACE-World-Model collection created
- [ ] All project documents ingested
- [ ] Python wrapper can query successfully
- [ ] SMFOI-KERNEL can invoke World Model
- [ ] C-index calculation operational in DigitalDNA