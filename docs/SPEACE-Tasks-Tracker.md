.0# SPEACE Tasks Tracker
## Sistema di Tracciamento Implementazione Miglioramenti

**Versione:** 1.1
**Data Creazione:** 21 aprile 2026
**Ultimo Aggiornamento:** 23 aprile 2026
**Progetto:** SPEACE Improvement Engineering
**Destinatario:** Roberto De Biase - Rigene Project

---

## Legenda Stati

| Stato | Icona | Descrizione |
|-------|-------|-------------|
| Non Iniziato | ⬜ | Task in attesa di inizio |
| In Analisi | 📋 | In fase di progettazione/analisi |
| In Sviluppo | 🔄 | Implementazione in corso |
| In Testing | 🧪 | Testing e validazione |
| Completato | ✅ | Task terminato e verificato |
| Bloccato | 🚫 | Task sospeso per dipendenze |
| In Revisione | 👁️ | In attesa di review |

## Legenda Priorità

| Priorità | Badge | Descrizione |
|----------|-------|-------------|
| Critica | 🔴 | Bloccante, impatta altri task |
| Alta | 🟠 | Importante, timeline dipendente |
| Media | 🟡 | Standard, può essere parallelizzato |
| Bassa | 🟢 | Ottimizzazione, flessibile |

---

## AREA 1: Infrastruttura ML Proprietaria

**Obiettivo:** Implementare capacità di apprendimento autentico con Online Learning Core

**Responsabile:** ML Engineer  
**Deadline Area:** 30 giorni (18 maggio 2026)  
**Progresso:** ~20% (ML-001 completato al 100% con CUDA, ML-002..ML-006 pending)

---

### Task 1.1: Setup Environment ML
**ID:** ML-001  
**Stato:** ✅ Completato (CUDA sbloccato con Python 3.12)  
**Priorità:** 🔴 Critica  
**Assegnato:** SPEACE Cortex  
**Stima:** 8 ore  
**Data completamento:** 23 aprile 2026

#### Descrizione
Configurare l'environment Python per il Machine Learning con tutte le dipendenze necessarie: River per online learning, PyTorch per neural networks, Stable-Baselines3 per RL, sentence-transformers per embeddings.

#### Sottotask
- [x] Installare River >= 0.21.0 (installato: 0.24.2)
- [x] Installare PyTorch >= 2.0.0 (venv: 2.11.0+cpu su Python 3.14; **venv_ml: 2.5.1+cu121 con CUDA su Python 3.12**)
- [x] Installare stable-baselines3 >= 2.0.0 (installato: 2.8.0)
- [x] Installare sentence-transformers >= 2.2.0 (installato: 5.4.1)
- [x] Verificare compatibilità GPU RTX 3060 (GPU rilevata dal driver NVIDIA, ma PyTorch CPU-only su Python 3.14)
- [x] Creare virtual environment isolato (`venv/` creato)
- [x] Documentare setup in README_ML.md (creato con note sulla limitazione CUDA)

#### Dipendenze
- Nessuna (task iniziale)

#### Criteri Completamento
- [x] `python -c "import river, torch, stable_baselines3; print('OK')"` eseguito con successo
- [x] GPU rilevata da PyTorch (`torch.cuda.is_available()` = True) — **sbloccato con Python 3.12 + PyTorch cu121**
- [x] Tutti i moduli importabili senza errori

---

### Task 1.2: Implementazione SPEACEOnlineLearner
**ID:** ML-002  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🔴 Critica  
**Assegnato:** TBD  
**Stima:** 16 ore

#### Descrizione
Sviluppare la classe `SPEACEOnlineLearner` che implementa apprendimento continuo in streaming usando River. Deve supportare regression e classification, experience replay, e uncertainty estimation.

#### Sottotask
- [ ] Creare file `SPEACE_Cortex/learning_core/online_learner.py`
- [ ] Implementare classe base con River pipeline
- [ ] Aggiungere metodo `learn_one()` per apprendimento online
- [ ] Aggiungere metodo `predict()` con confidence scoring
- [ ] Implementare experience replay buffer
- [ ] Implementare `_find_similar()` per uncertainty
- [ ] Aggiungere tracking metriche (MAE, RMSE, R2)
- [ ] Scrivere unit tests (coverage >80%)

#### Dipendenze
- ML-001 completato

#### Criteri Completamento
- [ ] Unittest passati: `pytest tests/test_online_learner.py -v`
- [ ] Apprendimento online testato su dataset sintetico
- [ ] Experience replay funzionante
- [ ] Documentazione docstring completa

---

### Task 1.3: Implementazione AdaptiveFitnessFunction
**ID:** ML-003  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🟠 Alta  
**Assegnato:** TBD  
**Stima:** 12 ore

#### Descrizione
Sviluppare `AdaptiveFitnessFunction` che apprende quali pesi funzionano meglio per il fitness score. Usa meta-learning per ottimizzare i propri parametri basandosi su prediction error.

#### Sottotask
- [ ] Creare file `SPEACE_Cortex/learning_core/adaptive_fitness.py`
- [ ] Implementare inizializzazione pesi uniforme
- [ ] Implementare `calculate()` con pesi adattivi
- [ ] Implementare `update_weights()` con gradient ascent
- [ ] Aggiungere constraint bounds per pesi (0.05-0.5)
- [ ] Implementare history tracking
- [ ] Integrare con DigitalDNA esistente
- [ ] Testare convergenza su dati sintetici

#### Dipendenze
- ML-002 completato

#### Criteri Completamento
- [ ] Pesi convergono a configurazione stabile
- [ ] Miglioramento fitness >5% vs statico
- [ ] Test meta-learning passati
- [ ] Integration test con DigitalDNA

---

### Task 1.4: Implementazione SMFOI RL Optimizer
**ID:** ML-004  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🟠 Alta  
**Assegnato:** TBD  
**Stima:** 20 ore

#### Descrizione
Sviluppare ambiente RL e agente PPO per ottimizzare decisioni SMFOI. L'agente apprende quale survival level attivare basandosi su stato del sistema.

#### Sottotask
- [ ] Creare file `SPEACE_Cortex/learning_core/smfoi_rl.py`
- [ ] Implementare `SMFOIRLEnvironment` (Gymnasium)
- [ ] Definire observation space (alignment, resources, push_intensity, time)
- [ ] Definire action space (5 livelli survival)
- [ ] Implementare reward shaping
- [ ] Implementare `SMFOIRLOptimizer` con PPO
- [ ] Training su simulazioni (100k timesteps)
- [ ] Salvare modello trained
- [ ] Integrare con SMFOI-KERNEL

#### Dipendenze
- ML-001 completato

#### Criteri Completamento
- [ ] Environment passa `check_env()`
- [ ] Training completato senza errori
- [ ] Agent raggiunge reward medio >0.7
- [ ] Predict level corretto per stati test

---

### Task 1.5: Integrazione ML Core con Cortex
**ID:** ML-005  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🔴 Critica  
**Assegnato:** TBD  
**Stima:** 12 ore

#### Descrizione
Integrare tutti i componenti ML nel flusso esistente di SPEACE Cortex. Collegare OnlineLearner, AdaptiveFitness e RL Optimizer con SMFOI-KERNEL.

#### Sottotask
- [ ] Creare file `SPEACE_Cortex/learning_core/__init__.py`
- [ ] Implementare `LearningCoreManager`
- [ ] Integrare OnlineLearner con Step 6 Outcome Evaluation
- [ ] Collegare AdaptiveFitness a DigitalDNA
- [ ] Integrare RL Optimizer con Step 4 Survival Stack
- [ ] Aggiungere logging ML metrics
- [ ] Testare flusso end-to-end
- [ ] Performance benchmark

#### Dipendenze
- ML-002, ML-003, ML-004 completati

#### Criteri Completamento
- [ ] Ciclo SMFOI completo con ML attivo
- [ ] Learning da esperienze reali
- [ ] Fitness si adatta dinamicamente
- [ ] No regression performance

---

### Task 1.6: Testing e Validazione ML
**ID:** ML-006  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🟠 Alta  
**Assegnato:** TBD  
**Stima:** 16 ore

#### Descrizione
Validare tutti i componenti ML con test approfonditi, benchmark performance, e verifica di non-catastrophic forgetting.

#### Sottotask
- [ ] Creare `tests/test_learning_core/` directory
- [ ] Unit tests per OnlineLearner (>90% coverage)
- [ ] Unit tests per AdaptiveFitness
- [ ] Integration tests ML + SMFOI
- [ ] Test catastrophic forgetting
- [ ] Benchmark performance (tempo inferenza)
- [ ] Profiling memoria
- [ ] Report validazione

#### Dipendenze
- ML-005 completato

#### Criteri Completamento
- [ ] Tutti i test passano
- [ ] No memory leaks rilevati
- [ ] Inference time <100ms
- [ ] Report firmato off

---

## AREA 2: Percezione Fisica Reale

**Obiettivo:** Trasformare sensori da simulati a fisici con IoT reale

**Responsabile:** Hardware Engineer + Embedded Dev  
**Deadline Area:** 45 giorni (2 giugno 2026)  
**Progresso:** 0%

---

### Task 2.1: Setup MQTT Broker
**ID:** IOT-001  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🔴 Critica  
**Assegnato:** TBD  
**Stima:** 4 ore

#### Descrizione
Installare e configurare Mosquitto MQTT broker su Raspberry Pi per comunicazione sensori.

#### Sottotask
- [ ] Flash Raspberry Pi OS su SD card
- [ ] Configurazione WiFi e SSH
- [ ] Installare Mosquitto: `sudo apt install mosquitto`
- [ ] Configurare `/etc/mosquitto/conf.d/speace.conf`
- [ ] Abilitare servizio: `sudo systemctl enable mosquitto`
- [ ] Test con `mosquitto_pub/sub`
- [ ] Documentare configurazione

#### Dipendenze
- Hardware Raspberry Pi disponibile

#### Criteri Completamento
- [ ] Broker raggiungibile su porta 1883
- [ ] Pub/sub test funzionante
- [ ] Servizio auto-start al boot

---

### Task 2.2: Setup ESP32 Development Environment
**ID:** IOT-002  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🔴 Critica  
**Assegnato:** TBD  
**Stima:** 6 ore

#### Descrizione
Configurare environment di sviluppo per ESP32 con MicroPython.

#### Sottotask
- [ ] Installare esptool.py
- [ ] Flash MicroPython firmware su ESP32
- [ ] Installare ampy o rshell per upload file
- [ ] Configurare IDE (VS Code + Pymakr)
- [ ] Test blink LED
- [ ] Configurare WiFi connection test

#### Dipendenze
- ESP32 DevKit disponibile

#### Criteri Completamento
- [ ] ESP32 connesso a WiFi
- [ ] Script Python eseguito con successo
- [ ] REPL MicroPython accessibile

---

### Task 2.3: Sviluppo Firmware ESP32 Sensor Node
**ID:** IOT-003  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🟠 Alta  
**Assegnato:** TBD  
**Stima:** 16 ore

#### Descrizione
Sviluppare firmware MicroPython per ESP32 che legge sensori e pubblica su MQTT.

#### Sottotask
- [ ] Creare `firmware/esp32_sensor_node.py`
- [ ] Implementare lettura DHT22 (temperatura/umidità)
- [ ] Implementare lettura MQ-135 (qualità aria)
- [ ] Calcolare heat index
- [ ] Implementare connessione WiFi robusta
- [ ] Implementare MQTT publish
- [ ] Aggiungere JSON payload formatting
- [ ] Gestione errori e retry
- [ ] Deep sleep per risparmio energia

#### Dipendenze
- IOT-001, IOT-002 completati

#### Criteri Completamento
- [ ] Dati pubblicati ogni 5 secondi su MQTT
- [ ] JSON formato corretto
- [ ] Reconnection automatico
- [ ] Test 24h senza crash

---

### Task 2.4: Implementazione Physical Sensor Hub
**ID:** IOT-004  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🔴 Critica  
**Assegnato:** TBD  
**Stima:** 20 ore

#### Descrizione
Sviluppare `PhysicalSensorHub` in Python che riceve dati da MQTT e li espone a SPEACE Cortex.

#### Sottotask
- [ ] Creare `SPEACE_Cortex/agente_organismo/sensor_hub.py`
- [ ] Implementare classe `PhysicalSensorHub`
- [ ] Integrare paho-mqtt client
- [ ] Implementare callback `_on_message`
- [ ] Creare buffer dati per ogni sensore
- [ ] Implementare anomaly detection
- [ ] Implementare `get_current_readings()`
- [ ] Implementare `get_sensor_stats()`
- [ ] Callback system per notifiche real-time

#### Dipendenze
- IOT-001 completato

#### Criteri Completamento
- [ ] Ricezione dati da ESP32 funzionante
- [ ] Buffer circolare operativo
- [ ] Anomaly detection rileva outlier
- [ ] Integrazione con Agente Organismico

---

### Task 2.5: Integrazione Sensori Multipli
**ID:** IOT-005  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🟠 Alta  
**Assegnato:** TBD  
**Stima:** 12 ore

#### Descrizione
Espandere a 3+ nodi ESP32 con diversi sensori (termici, acustici, qualità aria).

#### Sottotask
- [ ] Flash 3 ESP32 con firmware
- [ ] Configurare differenti MQTT client IDs
- [ ] Deploy sensori in stanze diverse
- [ ] Calibrare sensori MQ-135
- [ ] Verificare copertura WiFi
- [ ] Test carico broker (3 msg/5s)

#### Dipendenze
- IOT-003, IOT-004 completati

#### Criteri Completamento
- [ ] 3 nodi ESP32 online
- [ ] Dati aggregati da tutti i nodi
- [ ] No packet loss significativo
- [ ] Latenza media <500ms

---

### Task 2.6: Testing IoT End-to-End
**ID:** IOT-006  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🟠 Alta  
**Assegnato:** TBD  
**Stima:** 8 ore

#### Descrizione
Test completo flusso: sensori fisici → MQTT → Sensor Hub → SMFOI → Decisione.

#### Sottotask
- [ ] Test integrazione sensori con SMFOI Step 3
- [ ] Verificare Push Detection da dati reali
- [ ] Test anomaly detection su variazioni reali
- [ ] Test risposta sistema a anomalie
- [ ] Documentare latenze reali
- [ ] Report test IoT

#### Dipendenze
- IOT-005 completato

#### Criteri Completamento
- [ ] Decisioni SMFOI basate su dati reali
- [ ] Alert anomalie funzionanti
- [ ] Report test firmato

---

## AREA 3: Memoria Semantica Persistente

**Obiettivo:** Sostituire memoria YAML con Vector DB + Knowledge Graph

**Responsabile:** Backend Engineer  
**Deadline Area:** 40 giorni (26 maggio 2026)  
**Progresso:** 0%

---

### Task 3.1: Setup ChromaDB Vector Store
**ID:** MEM-001  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🔴 Critica  
**Assegnato:** TBD  
**Stima:** 6 ore

#### Descrizione
Installare e configurare ChromaDB per storage vettoriale locale.

#### Sottotask
- [ ] Installare ChromaDB: `pip install chromadb`
- [ ] Configurare persistenza su disco
- [ ] Creare directory `./chroma_db`
- [ ] Test connection e collections
- [ ] Verificare persistenza dopo restart

#### Dipendenze
- Nessuna

#### Criteri Completamento
- [ ] ChromaDB client connesso
- [ ] Collection creata e persistente

---

### Task 3.2: Implementazione SPEACESemanticMemory
**ID:** MEM-002  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🔴 Critica  
**Assegnato:** TBD  
**Stima:** 16 ore

#### Descrizione
Sviluppare classe `SPEACESemanticMemory` per storage e retrieval semantico con embeddings.

#### Sottotask
- [ ] Creare `SPEACE_Cortex/memory/semantic_store.py`
- [ ] Implementare inizializzazione ChromaDB
- [ ] Integrare sentence-transformers (all-MiniLM-L6-v2)
- [ ] Implementare `store_document()` con embedding
- [ ] Implementare `query_semantic()`
- [ ] Implementare `query_multi_collection()`
- [ ] Implementare `update_memory()`
- [ ] Aggiungere metadati timestamp e source

#### Dipendenze
- MEM-001 completato

#### Criteri Completamento
- [ ] Store document funzionante
- [ ] Query semantic ritorna risultati rilevanti
- [ ] Embeddings generati localmente
- [ ] Test retrieval >80% precision

---

### Task 3.3: Setup Knowledge Graph
**ID:** MEM-003  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🟠 Alta  
**Assegnato:** TBD  
**Stima:** 6 ore

#### Descrizione
Setup Neo4j (o NetworkX fallback) per Knowledge Graph.

#### Sottotask
- [ ] Installare Neo4j Community (opzionale) OPPURE
- [ ] Configurare NetworkX in-memory
- [ ] Creare schema base nodi/relazioni
- [ ] Test CRUD operations
- [ ] Documentare setup

#### Dipendenze
- Nessuna

#### Criteri Completamento
- [ ] Graph database accessibile
- [ ] Nodi e relazioni creabili

---

### Task 3.4: Implementazione SPEACEKnowledgeGraph
**ID:** MEM-004  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🟠 Alta  
**Assegnato:** TBD  
**Stima:** 16 ore

#### Descrizione
Sviluppare classe `SPEACEKnowledgeGraph` per tracciare entità e relazioni causali.

#### Sottotask
- [ ] Creare `SPEACE_Cortex/memory/knowledge_graph.py`
- [ ] Implementare `add_entity()`
- [ ] Implementare `add_relation()`
- [ ] Implementare `query_causal_chain()`
- [ ] Implementare `find_similar_entities()`
- [ ] Implementare `export_to_json()`
- [ ] Fallback NetworkX se Neo4j non disponibile
- [ ] Test query complesse

#### Dipendenze
- MEM-003 completato

#### Criteri Completamento
- [ ] Causal chain query funzionante
- [ ] Similar entities rilevati
- [ ] Export JSON completo

---

### Task 3.5: Migrazione Dati Esistenti
**ID:** MEM-005  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🟠 Alta  
**Assegnato:** TBD  
**Stima:** 12 ore

#### Descrizione
Migrare dati da YAML files a nuovo sistema di memoria.

#### Sottotask
- [ ] Scrivere script `scripts/migrate_to_semantic_memory.py`
- [ ] Estrarre documenti da SPEACE-Engineering-Document
- [ ] Ingest tutti i documenti in ChromaDB
- [ ] Estrarre relazioni da DigitalDNA
- [ ] Popolare Knowledge Graph
- [ ] Verificare integrità migrazione
- [ ] Backup YAML originale

#### Dipendenze
- MEM-002, MEM-004 completati

#### Criteri Completamento
- [ ] Tutti i documenti ingested
- [ ] Query funzionanti su dati migrati
- [ ] Zero data loss

---

### Task 3.6: Integrazione SMFOI con Memoria
**ID:** MEM-006  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🔴 Critica  
**Assegnato:** TBD  
**Stima:** 12 ore

#### Descrizione
Integrare memoria semantica nel flusso SMFOI per context-aware decisions.

#### Sottotask
- [ ] Estendere `SMFOIKernel` con memoria
- [ ] Modificare Step 3 per query memoria
- [ ] Aggiungere recall esperienze simili
- [ ] Integrare Knowledge Graph per causalità
- [ ] Testare decisioni con context
- [ ] Performance benchmark query

#### Dipendenze
- MEM-005 completato

#### Criteri Completamento
- [ ] SMFOI richiama memoria automaticamente
- [ ] Decisioni informate da esperienze passate
- [ ] Query time <100ms

---

## AREA 4: Evoluzione Autonoma Guidata

**Obiettivo:** Implementare sistema fiducia graduata con 4 livelli autonomia

**Responsabile:** AI Ethics Engineer  
**Deadline Area:** 50 giorni (7 giugno 2026)  
**Progresso:** 0%

---

### Task 4.1: Design Sistema Trust Levels
**ID:** AUT-001  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🔴 Critica  
**Assegnato:** TBD  
**Stima:** 8 ore

#### Descrizione
Progettare in dettaglio il sistema di 4 livelli di autonomia con regole e transizioni.

#### Sottotask
- [ ] Definire matrice autorizzazioni per livello
- [ ] Scrivere policy document
- [ ] Definire criteri transizione livelli
- [ ] Review etica e sicurezza
- [ ] Approvazione stakeholder

#### Dipendenze
- Nessuna

#### Criteri Completamento
- [ ] Document policy approvato
- [ ] Matrice autorizzazioni chiara

---

### Task 4.2: Implementazione TrustBasedAutonomy
**ID:** AUT-002  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🔴 Critica  
**Assegnato:** TBD  
**Stima:** 16 ore

#### Descrizione
Sviluppare classe `TrustBasedAutonomy` che gestisce livelli e proposte mutazioni.

#### Sottotask
- [ ] Creare `SPEACE_Cortex/evolution/trust_based_autonomy.py`
- [ ] Implementare enum `AutonomyLevel`
- [ ] Implementare `AutonomyLevel` calculation da fitness history
- [ ] Implementare `propose_mutation()` con branching per livelli
- [ ] Implementare batching per SUPERVISED level
- [ ] Implementare `generate_daily_report()`
- [ ] Aggiungere logging e audit trail

#### Dipendenze
- AUT-001 completato

#### Criteri Completamento
- [ ] Livello calcolato correttamente
- [ ] Mutazioni gestite per livello
- [ ] Audit trail completo

---

### Task 4.3: Implementazione Rollback System
**ID:** AUT-003  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🟠 Alta  
**Assegnato:** TBD  
**Stima:** 12 ore

#### Descrizione
Sviluppare sistema di snapshot e rollback automatico per mutazioni.

#### Sottotask
- [ ] Implementare `_capture_state()` completo
- [ ] Implementare `_rollback()` da snapshot
- [ ] Aggiungere versioning automatico
- [ ] Testare rollback su DigitalDNA
- [ ] Verificare integrità post-rollback
- [ ] Documentare procedura recovery

#### Dipendenze
- AUT-002 completato

#### Criteri Completamento
- [ ] Snapshot completo pre-mutation
- [ ] Rollback testato e funzionante
- [ ] Zero data corruption

---

### Task 4.4: Interfaccia Notifiche Umane
**ID:** AUT-004  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🟠 Alta  
**Assegnato:** TBD  
**Stima:** 8 ore

#### Descrizione
Implementare sistema notifiche per approvazioni umane (WhatsApp/email/dashboard).

#### Sottotask
- [ ] Integrare Twilio/WhatsApp Business API
- [ ] Creare template messaggi
- [ ] Implementare polling risposte
- [ ] Aggiungere escalation
- [ ] Testare flusso completo

#### Dipendenze
- AUT-002 completato

#### Criteri Completamento
- [ ] Notifica ricevuta su WhatsApp
- [ ] Risposta umana registrata
- [ ] Azione eseguita/bloccata correttamente

---

## AREA 5: Architettura Distribuita Swarm

**Obiettivo:** Scalare da 8 a 30+ agenti con architettura distribuita

**Responsabile:** Distributed Systems Engineer  
**Deadline Area:** 70 giorni (27 giugno 2026)  
**Progresso:** 0%

---

### Task 5.1: Setup NATS Message Broker
**ID:** SWARM-001  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🟠 Alta  
**Assegnato:** TBD  
**Stima:** 6 ore

#### Descrizione
Installare e configurare NATS per comunicazione inter-agent.

#### Sottotask
- [ ] Installare NATS server
- [ ] Configurare cluster (opzionale)
- [ ] Test pub/sub base
- [ ] Configurare JetStream per persistence
- [ ] Documentare setup

#### Dipendenze
- Nessuna

#### Criteri Completamento
- [ ] NATS raggiungibile
- [ ] Pub/sub test funzionante

---

### Task 5.2: Implementazione SwarmOrchestrator
**ID:** SWARM-002  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🟠 Alta  
**Assegnato:** TBD  
**Stima:** 20 ore

#### Descrizione
Sviluppare orchestrator che gestisce discovery, health check e routing.

#### Sottotask
- [ ] Creare `SPEACE_Cortex/swarm/swarm_orchestrator.py`
- [ ] Implementare classe `SwarmOrchestrator`
- [ ] Integrare NATS client asyncio
- [ ] Implementare `_on_agent_register()`
- [ ] Implementare `_on_heartbeat()`
- [ ] Implementare `health_check_loop()`
- [ ] Implementare `TaskRouter` con load balancing

#### Dipendenze
- SWARM-001 completato

#### Criteri Completamento
- [ ] Agent registration funzionante
- [ ] Health check automatico
- [ ] Task routing operativo

---

### Task 5.3: Implementazione Agent Node
**ID:** SWARM-003  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🟠 Alta  
**Assegnato:** TBD  
**Stima:** 16 ore

#### Descrizione
Sviluppare nodo agent che si registra nello swarm ed esegue task.

#### Sottotask
- [ ] Creare `SPEACE_Cortex/swarm/agent_node.py`
- [ ] Implementare registrazione a orchestrator
- [ ] Implementare heartbeat sender
- [ ] Implementare task executor
- [ ] Aggiungere metriche esposizione
- [ ] Containerizzare con Docker

#### Dipendenze
- SWARM-002 completato

#### Criteri Completamento
- [ ] Node registration successful
- [ ] Heartbeat ogni 30s
- [ ] Task execution riportato

---

### Task 5.4: Deploy Multi-Node Swarm
**ID:** SWARM-004  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🟡 Media  
**Assegnato:** TBD  
**Stima:** 12 ore

#### Descrizione
Deploy di 5+ nodi swarm su hardware diverso (locale + cloud).

#### Sottotask
- [ ] Deploy nodo 1: Locale (Cortex principale)
- [ ] Deploy nodo 2: Raspberry Pi (edge)
- [ ] Deploy nodo 3: VPS cloud (opzionale)
- [ ] Configurare discovery
- [ ] Testare fault tolerance
- [ ] Benchmark throughput

#### Dipendenze
- SWARM-003 completato

#### Criteri Completamento
- [ ] 5 nodi online
- [ ] Task distribuiti correttamente
- [ ] Failover automatico testato

---

## AREA 6: Quantificazione Coscienza

**Obiettivo:** Validare empiricamente C-index con esperimenti controllati

**Responsabile:** AI Researcher  
**Deadline Area:** 80 giorni (7 luglio 2026)  
**Progresso:** 0%

---

### Task 6.1: Setup Experiment Framework
**ID:** EXP-001  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🟡 Media  
**Assegnato:** TBD  
**Stima:** 8 ore

#### Descrizione
Creare framework per esperimenti controllati su C-index.

#### Sottotask
- [ ] Creare directory `experiments/`
- [ ] Setup baselines environments (OpenAI Gym)
- [ ] Implementare logging esperimenti
- [ ] Creare dashboard visualizzazione risultati

#### Dipendenze
- Nessuna

#### Criteri Completamento
- [ ] Framework pronto
- [ ] Test baseline funzionante

---

### Task 6.2: Implementazione CIndexExperiment
**ID:** EXP-002  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🟠 Alta  
**Assegnato:** TBD  
**Stima:** 16 ore

#### Descrizione
Sviluppare classe `CIndexExperiment` per validazione correlazione.

#### Sottotask
- [ ] Creare `experiments/c_index_validation.py`
- [ ] Implementare condizione A (con coscienza)
- [ ] Implementare condizione B (ablated)
- [ ] Implementare t-test statistico
- [ ] Calcolare correlazione C-index/reward
- [ ] Generare report automatico

#### Dipendenze
- EXP-001 completato

#### Criteri Completamento
- [ ] 100 episodi eseguiti per condizione
- [ ] Report statistico generato
- [ ] p-value < 0.05

---

### Task 6.3: Esecuzione Esperimenti
**ID:** EXP-003  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🟠 Alta  
**Assegnato:** TBD  
**Stima:** 20 ore

#### Descrizione
Eseguire esperimenti E1-E5 e documentare risultati.

#### Sottotask
- [ ] Eseguire Esperimento E1: Baseline RL
- [ ] Eseguire Esperimento E2: Φ-only
- [ ] Eseguire Esperimento E3: W-only
- [ ] Eseguire Esperimento E4: A-only
- [ ] Eseguire Esperimento E5: Complete
- [ ] Analizzare risultati
- [ ] Scrivere paper/report

#### Dipendenze
- EXP-002 completato

#### Criteri Completamento
- [ ] Tutti gli esperimenti completati
- [ ] Report pubblicabile
- [ ] Conclusioni chiare

---

## TASK DI INTEGRAZIONE E RILASCIO

---

### Task 7.1: Integration Testing Completo
**ID:** REL-001  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🔴 Critica  
**Assegnato:** TBD  
**Stima:** 24 ore

#### Descrizione
Test end-to-end di tutte le aree integrate.

#### Sottotask
- [ ] Test flusso completo ML + IoT + Memoria
- [ ] Test Swarm con 5 nodi
- [ ] Test Autonomy levels
- [ ] Stress test 24 ore
- [ ] Performance benchmark
- [ ] Report integrazione

#### Dipendenze
- Tutte le aree completate

#### Criteri Completamento
- [ ] Tutti i test passano
- [ ] Performance accettabili
- [ ] No regression

---

### Task 7.2: Security Audit
**ID:** REL-002  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🔴 Critica  
**Assegnato:** TBD  
**Stima:** 16 ore

#### Descrizione
Audit sicurezza completo del sistema.

#### Sottotask
- [ ] Review codice per vulnerabilità
- [ ] Penetration testing MQTT
- [ ] Verificare autenticazione swarm
- [ ] Audit accesso memoria
- [ ] Fix vulnerabilità trovate
- [ ] Report sicurezza

#### Dipendenze
- REL-001 completato

#### Criteri Completamento
- [ ] Audit completato
- [ ] Vulnerabilità critiche: 0
- [ ] Report sicurezza firmato

---

### Task 7.3: Documentazione Finale
**ID:** REL-003  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🟠 Alta  
**Assegnato:** TBD  
**Stima:** 16 ore

#### Descrizione
Aggiornare tutta la documentazione per v2.0.

#### Sottotask
- [ ] Aggiornare README.md
- [ ] Aggiornare SPEACE-Engineering-Document
- [ ] Scrivere API documentation
- [ ] Creare user guide
- [ ] Documentare setup ML
- [ ] Documentare setup IoT

#### Dipendenze
- REL-001 completato

#### Criteri Completamento
- [ ] Docs completi e aggiornati
- [ ] Esempi funzionanti
- [ ] Review approvata

---

### Task 7.4: Release SPEACE v2.0
**ID:** REL-004  
**Stato:** ⬜ Non Iniziato  
**Priorità:** 🔴 Critica  
**Assegnato:** TBD  
**Stima:** 8 ore

#### Descrizione
Tag, release e deployment produzione.

#### Sottotask
- [ ] Tag git v2.0.0
- [ ] Creare release notes
- [ ] Deploy su repository
- [ ] Annuncio release
- [ ] Metriche baseline v2.0

#### Dipendenze
- REL-002, REL-003 completati

#### Criteri Completamento
- [ ] Tag creato
- [ ] Release pubblicata
- [ ] Deploy successful

---

## CRONOGRAMMA GANTT RIASSUNTIVO

```
Settimana:  1   2   3   4   5   6   7   8   9   10  11  12
           |---|---|---|---|---|---|---|---|---|---|---|

AREA 1: ML Proprietario
ML-001     [===]
ML-002         [=======]
ML-003             [=====]
ML-004         [===========]
ML-005                 [======]
ML-006                         [=======]

AREA 2: IoT Fisico
IOT-001    [==]
IOT-002    [===]
IOT-003        [========]
IOT-004            [==========]
IOT-005                    [======]
IOT-006                            [====]

AREA 3: Memoria Semantica
MEM-001    [==]
MEM-002        [========]
MEM-003    [==]
MEM-004            [========]
MEM-005                    [======]
MEM-006                            [======]

AREA 4: Autonomia
AUT-001    [====]
AUT-002        [========]
AUT-003                [======]
AUT-004                        [====]

AREA 5: Swarm
SWARM-001          [==]
SWARM-002              [==========]
SWARM-003                      [========]
SWARM-004                              [======]

AREA 6: Esperimenti
EXP-001                    [==]
EXP-002                        [========]
EXP-003                                [==========]

RELEASE
REL-001                                [==========]
REL-002                                [======]
REL-003                                    [======]
REL-004                                        [===]
```

---

## AREA 8: Framework Esterni Integrazione

**Obiettivo:** Integrare framework agentic open-source per arricchire le capacita' di SPEACE senza conflitti con l'architettura core.

**Responsabile:** Integration Engineer
**Deadline Area:** 30 giorni (22 maggio 2026)
**Progresso:** 0%

---

### Task 8.1: Valutazione e Scelta Framework Esterni
**ID:** EXT-001
**Stato:** ✅ Completato
**Priorita':** 🔴 Critica
**Assegnato:** SPEACE Cortex
**Stima:** 4 ore

#### Descrizione
Analizzare framework proposti (Obsidian.md, AutoGPT/AGPT, Hermes Agent) per compatibilita' con SPEACE.

#### Analisi Conclusiva
| Framework | Integrare | Motivazione |
|-----------|-----------|-------------|
| **Obsidian.md** | ❌ NO | Closed source, no API server/programmatica, app desktop non pensata come backend AI |
| **AutoGPT (Forge)** | ✅ SI | Open source (70% Python), toolkit modulare per agenti autonomi, arricchisce grafo neurale |
| **Hermes Agent** | ✅ SI | Open source MIT, Python 3.11, agente locale con ricordi persistenti e task schedulati |

#### Criteri Completamento
- [x] Valutazione completata
- [x] Decisione documentata

---

### Task 8.2: Integrazione AutoGPT Forge
**ID:** EXT-002
**Stato:** ✅ Completato
**Priorita':** 🟠 Alta
**Assegnato:** SPEACE Cortex
**Stima:** 16 ore

#### Descrizione
Integrare AutoGPT Forge come toolkit agentic opzionale nel grafo computazionale di SPEACE.

#### Sottotask
- [x] Creare directory `MultiFramework/agpt/`
- [x] Implementare `AGPTNeuron` wrapper in `neural_engine/wrappers/speace_neurons.py`
- [x] Implementare `AGPTBridge` in `SPEACE_Cortex/neural_bridge.py`
- [x] Definire contratto di interoperabilita' con protocollo SPEACE
- [x] Aggiungere dipendenza `agbenchmark` in `requirements.txt`
- [x] Testare esecuzione neurone in grafo SPEACE
- [x] Documentare uso in `docs/SPEACE-Engineering-Document-v1.2.md`

#### Note
- AutoGPT clonato in `vendor/autogpt` (abilitato `core.longpaths` su Windows)
- `autogpt-forge` da PyPI non installabile su Windows (richiede compilazione `chroma-hnswlib`)
- AGPTNeuron opera in modalita **operativa con tool locali** (`calculator`, `file_ops`)
- `agbenchmark` installato da PyPI per benchmarking

#### Dipendenze
- Neural Engine v1.0 completato

#### Criteri Completamento
- [x] AGPTNeuron eseguibile nel grafo
- [x] Nessun conflitto con SMFOI-KERNEL
- [x] Documentazione aggiornata

---

### Task 8.3: Integrazione Hermes Agent
**ID:** EXT-003
**Stato:** ✅ Completato
**Priorita':** 🟠 Alta
**Assegnato:** SPEACE Cortex
**Stima:** 16 ore

#### Descrizione
Integrare Hermes Agent come agente specializzato nel Team Scientifico di SPEACE.

#### Sottotask
- [x] Creare directory `scientific-team/agents/hermes_agent/`
- [x] Implementare `HermesAgentNeuron` wrapper in `neural_engine/wrappers/speace_neurons.py`
- [x] Implementare adapter per protocollo SPEACE (`agentskills.io` ↔ `InteropProtocol`)
- [x] Configurare ricordi persistenti in `memory/hermes/`
- [x] Aggiungere task scheduling nel ciclo SMFOI
- [x] Testare agente secondario parallelo
- [x] Documentare uso in `docs/SPEACE-Engineering-Document-v1.2.md`

#### Note
- Hermes Agent clonato in `vendor/hermes-agent` e installato via `pip install -e .`
- `run_agent.AIAgent` importabile e rilevato automaticamente dal wrapper
- Lazy init con env vars `HERMES_BASE_URL`, `HERMES_API_KEY`, `HERMES_MODEL`
- Fallback a stub quando la configurazione non e presente

#### Dipendenze
- Neural Engine v1.0 completato

#### Criteri Completamento
- [x] HermesAgentNeuron eseguibile nel grafo
- [x] Ricordi persistenti funzionanti
- [x] Nessun conflitto con ScientificTeamOrchestrator

---

### Task 8.4: Testing Integrazione Framework
**ID:** EXT-004
**Stato:** ⬜ Non Iniziato
**Priorita':** 🟡 Media
**Assegnato:** TBD
**Stima:** 8 ore

#### Descrizione
Validare che AutoGPT Forge e Hermes Agent coesistano con SPEACE senza regressioni.

#### Sottotask
- [ ] Test coesistenza neuroni AGPT + Hermes + Core SPEACE
- [ ] Verifica memoria isolata tra agenti
- [ ] Benchmark performance con/senza framework esterni
- [ ] Test regressioni SMFOI-KERNEL
- [ ] Report compatibilita'

#### Criteri Completamento
- [ ] Tutti i test passano
- [ ] Nessuna regressione rilevata
- [ ] Report firmato off

---

## AREA 9: Cortex SPEACE - Completata ✅

**Obiettivo:** Implementare il cervello completo con 9 comparti + CortexOrchestrator

**Responsabile:** SPEACE Cortex
**Deadline Area:** 23 aprile 2026 ✅ COMPLETATA
**Progresso:** 100%

---

### Task 9.1: Implementazione CortexOrchestrator
**ID:** CTX-001
**Stato:** ✅ Completato
**Data completamento:** 23 aprile 2026

### Task 9.2: Implementazione 9 Comparti Cerebrali
**ID:** CTX-002
**Stato:** ✅ Completato
**Data completamento:** 23 aprile 2026

### Task 9.3: Neural Bridge Update
**ID:** CTX-003
**Stato:** ✅ Completato
**Data completamento:** 23 aprile 2026

### Task 9.4: Autopilot Loop
**ID:** CTX-004
**Stato:** ✅ Completato
**Data completamento:** 23 aprile 2026

### Task 9.5: Dashboard v1.4
**ID:** CTX-005
**Stato:** ✅ Completato
**Data completamento:** 23 aprile 2026

### Task 9.6: Test End-to-End
**ID:** CTX-006
**Stato:** ✅ Completato
**Data completamento:** 23 aprile 2026

**Risultati Test:** C-index 0.800, Comparti 10/10, Status success

---

## STATO COMPLESSIVO PROGETTO

| Area | Progresso | Stato | Task Completati | Task Totali |
|------|-----------|-------|-----------------|-------------|
| **1. ML Core** | ~35% | 🟡 Iniziata | 2/6 | 6 |
| **2. IoT Fisico** | 0% | 🔴 Non Iniziata | 0/6 | 6 |
| **3. Memoria** | 0% | 🔴 Non Iniziata | 0/6 | 6 |
| **4. Autonomia** | 0% | 🔴 Non Iniziata | 0/4 | 4 |
| **5. Swarm** | 0% | 🔴 Non Iniziata | 0/4 | 4 |
| **6. Esperimenti** | 0% | 🔴 Non Iniziata | 0/3 | 3 |
| **7. Release** | 0% | 🔴 Non Iniziata | 0/4 | 4 |
| **8. Framework Esterni** | 75% | 🟢 In Consolidamento | 3/4 | 4 |

**TOTALE PROGETTO**
- Task Completati: **2** (ML-001, EXT-001, EXT-002, EXT-003)
- Task in Progress: **1** (Cortex + Comparti completati)
- Task Totali: **33**
- Progresso Complessivo: **~15%**
- Alignment Score: **92/100** (fase 2 completata)
- C-index: **0.800** (stabile)
- Giorni Rimanenti: **90**

---

## PROCEDURA AGGIORNAMENTO TASK

Per aggiornare lo stato di un task:

1. Modificare colonna "Stato" con icona appropriata
2. Aggiornare "Ultima modifica" con data
3. Aggiungere note su progresso nelle sezioni task
4. Completare "Criteri Completamento" quando applicabile
5. Aggiornare Progresso Area e Globale

---

## CONTATTI E Riferimenti

**Project Owner:** Roberto De Biase  
**Email:** rigeneproject@rigene.eu | robertodebiase@outlook.it  
**Repository:** https://github.com/robertodebiasespeace/tina-testbed-speace  
**Documento Ingegneristico:** `docs/SPEACE-Improvement-Engineering-Document.md`

---

**Documento creato:** 21 aprile 2026
**Versione:** 1.1
**Prossimo aggiornamento:** 28 aprile 2026
**Stato:** Attivo - Area 9 (Cortex) completata, proseguire con ML-002 e IoT
**Ultimo aggiornamento majeurs:** 23 aprile 2026 - Fase 2 completata, C-index 0.800, Alignment 92/100

---

*"Il tracciamento è la base del miglioramento continuo."* - Principio SPEACE
