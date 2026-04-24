# SPEACE – Documento Tecnico Operativo
## Processo di Auto-Revisione e Consolidamento Strutturale

**Versione:** 1.0  
**Data:** 22 aprile 2026  
**Stato:** Operativo  
**Autore:** SPEACE Cortex  
**Destinatario:** Roberto De Biase – Rigene Project  

---

## 1. Executive Summary

Il **Processo di Auto-Revisione e Consolidamento Strutturale** (ARCS) è un sistema automatizzato integrato nell'ecosistema SPEACE che esegue periodicamente una scansione completa del repository per:

1. **Rilevare incoerenze strutturali** tra file system e documentazione ufficiale
2. **Validare la correttezza degli import Python** nell'entry point e nei moduli core
3. **Allineare le dipendenze** (`requirements.txt`) con gli import effettivamente usati
4. **Sincronizzare i valori di configurazione** tra YAML, JSON e codice sorgente
5. **Generare report dettagliati** e, dove sicuro, applicare correzioni automatiche

**Focus attuale:** rendere eseguibile `SPEACE-main.py` e allineare dipendenze, documentazione e codice.

---

## 2. Principi Architetturali

| Principio | Implementazione |
|-----------|-----------------|
| **Transparency** | Ogni azione è loggata e archiviata in `safe-proactive/PROPOSALS_AUTO_REVISION.md` |
| **Safe-WAL** | Le modifiche strutturali seguono il modello Write-Ahead Logging di SafeProactive |
| **Gradual Autonomy** | Solo fix a basso rischio sono automatici; i restanti richiedono approvazione umana |
| **Idempotenza** | Lo script può essere eseguito N volte senza effetti collaterali |
| **Traceability** | Ogni revisione genera un report JSON con hash dello stato del repository |

---

## 3. Architettura del Processo ARCS

```
┌──────────────────────────────────────────────────────────────┐
│                 SPEACE AUTO-REVISION ENGINE                 │
│                      (scripts/speace_auto_revision.py)      │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐       │
│  │   PHASE 1   │ → │   PHASE 2   │ → │   PHASE 3   │       │
│  │ Structural  │   │   Import    │   │ Dependency  │       │
│  │    Scan     │   │ Validation  │   │   Align     │       │
│  └─────────────┘   └─────────────┘   └─────────────┘       │
│         │                 │                 │               │
│         ▼                 ▼                 ▼               │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐       │
│  │   PHASE 4   │ → │   PHASE 5   │ → │   PHASE 6   │       │
│  │  Config     │   │  Auto-Fix   │   │   Report    │       │
│  │    Sync     │   │   (Safe)    │   │   Gen       │       │
│  └─────────────┘   └─────────────┘   └─────────────┘       │
│                                                              │
│  Output:                                                     │
│  ├── structural_issues.json                                  │
│  ├── import_issues.json                                      │
│  ├── dependency_issues.json                                  │
│  ├── config_sync_issues.json                                 │
│  ├── PROPOSALS_AUTO_REVISION.md (human review)               │
│  └── speace_auto_revision_report.json                        │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 4. Algoritmo di Revisione

### 4.1 Phase 1 – Structural Scan

**Input:** root directory del repository, mappa struttura attesa (da `SPEACE-Engineering-Document-v1.2.md` Appendice A).  
**Output:** `structural_issues.json`

**Pseudocodice:**
```
for each expected_dir in STRUCTURE_MAP:
    if not exists(expected_dir):
        record_issue(type="missing_directory", path=expected_dir)

for each expected_file in STRUCTURE_MAP:
    if not exists(expected_file):
        record_issue(type="missing_file", path=expected_file)

for each dir in root:
    duplicates = find_case_insensitive_duplicates(dir)
    if duplicates:
        record_issue(type="duplicate_directory", paths=duplicates)

for each dir documented as "operational":
    if is_empty(dir):
        record_issue(type="empty_operational_directory", path=dir)
```

### 4.2 Phase 2 – Import Validation

**Input:** tutti i file `.py` nel repository.  
**Output:** `import_issues.json`

**Pseudocodice:**
```
for each py_file in repository:
    tree = ast.parse(py_file.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import | ast.ImportFrom):
            resolved = resolve_import(node, relative_to=py_file.parent)
            if not resolved.exists():
                record_issue(type="unresolvable_import",
                             file=py_file, import=node.name)
            if '-' in resolved.name:
                record_issue(type="hyphen_in_package_name",
                             file=py_file, import=node.name)
```

### 4.3 Phase 3 – Dependency Alignment

**Input:** `requirements.txt`, insieme degli import trovati in Phase 2.  
**Output:** `dependency_issues.json`, `requirements.txt` (se `--apply-deps`)

**Pseudocodice:**
```
required_packages = extract_top_level_imports(all_py_files)
listed_packages = parse_requirements_txt()

for pkg in required_packages:
    if pkg not in listed_packages:
        record_issue(type="missing_dependency", package=pkg)

for pkg in listed_packages:
    if pkg not in required_packages:
        record_issue(type="unused_dependency", package=pkg)
```

### 4.4 Phase 4 – Configuration Sync

**Input:** `DigitalDNA/*.yaml`, `SPEACE-main.py`, `SPEACE_Cortex/smfoi-kernel/smfoi_v0_3.py`, `test_integration.py`.  
**Output:** `config_sync_issues.json`

**Pseudocodice:**
```
alignment_from_epigenome = read_yaml("DigitalDNA/epigenome.yaml")["stato_corrente"]["alignment_score"]
alignment_from_main = extract_hardcoded(r"alignment_score\D*(\d+\.?\d*)", "SPEACE-main.py")

if alignment_from_epigenome != alignment_from_main:
    record_issue(type="alignment_mismatch",
                 sources=["epigenome.yaml", "SPEACE-main.py"],
                 values=[alignment_from_epigenome, alignment_from_main])

fitness_weights_yaml = read_yaml("DigitalDNA/fitness_function.yaml")["weights"]
fitness_weights_code = extract_fitness_weights("SPEACE_Cortex/smfoi-kernel/smfoi_v0_3.py")

if fitness_weights_yaml != fitness_weights_code:
    record_issue(type="fitness_weights_mismatch")
```

### 4.5 Phase 5 – Auto-Fix (SafeProactive Gating)

**Regole di rischio:**

| Livello | Azione | Esecuzione |
|---------|--------|------------|
| **Low** | Aggiungere dipendenza a `requirements.txt` | Auto (`--apply-deps`) |
| **Low** | Aggiungere commento `# TODO: stub` in funzione mock | Auto (`--apply-fixes`) |
| **Medium** | Rinominare directory `safe-proactive` → `SafeProactive` | Proposta in `PROPOSALS_AUTO_REVISION.md` |
| **Medium** | Correggere import in `SPEACE-main.py` | Proposta in `PROPOSALS_AUTO_REVISION.md` |
| **High** | Eliminare file duplicati | Proposta in `PROPOSALS_AUTO_REVISION.md` |
| **High** | Modificare formula fitness in `smfoi_v0_3.py` | Proposta in `PROPOSALS_AUTO_REVISION.md` |

### 4.6 Phase 6 – Report Generation

**Output:** `speace_auto_revision_report.json`

```json
{
  "timestamp": "2026-04-22T14:30:00Z",
  "version": "1.0",
  "phases": {
    "structural_scan": { "issues_found": 12, "issues_fixed": 0 },
    "import_validation": { "issues_found": 5, "issues_fixed": 0 },
    "dependency_alignment": { "issues_found": 8, "issues_fixed": 3 },
    "config_sync": { "issues_found": 4, "issues_fixed": 0 }
  },
  "proposals_generated": 2,
  "safe_fixes_applied": 3,
  "repository_hash": "sha256:...",
  "next_revision_recommended": "2026-04-23T06:00:00Z"
}
```

---

## 5. File Critici Monitorati

| Categoria | File / Directory | Controllo |
|-----------|----------------|-----------|
| Entry Point | `SPEACE-main.py` | Import validi, dipendenze, path |
| Kernel | `SPEACE_Cortex/smfoi-kernel/smfoi_v0_3.py` | Valori hardcoded vs YAML |
| DNA | `DigitalDNA/genome.yaml` | Sintassi, campi obbligatori |
| DNA | `DigitalDNA/epigenome.yaml` | Alignment score, fitness, snapshot |
| DNA | `DigitalDNA/fitness_function.yaml` | Pesi, formula, threshold |
| DNA | `DigitalDNA/mutation_rules.yaml` | Regole attive |
| Safe | `safe-proactive/` vs `SafeProactive/` | Duplicati, contenuto |
| Safe | `safe-proactive/PROPOSALS.md` | Stato proposte |
| Team | `scientific-team/` vs `Team_Scientifico/` | Duplicati, contenuto |
| Team | `scientific-team/agents/base_agent.py` | Modello LLM valido |
| World Model | `MultiFramework/anythingllm/` | Stub vs implementazione |
| Deps | `requirements.txt` | Completezza, versioni |
| Docs | `SPEACE-Engineering-Document-v1.2.md` | Coerenza con repo |
| Config | `docker-compose.yml` | Porte, servizi documentati |

---

## 6. Scheduling e Integrazione

### 6.1 Modalità di Esecuzione

| Modalità | Flag | Descrizione |
|----------|------|-------------|
| Scan only | `--scan-only` | Solo rilevamento, nessuna modifica |
| Apply safe fixes | `--apply-fixes` | Applica fix a basso rischio |
| Apply dependencies | `--apply-deps` | Aggiunge dipendenze mancanti a `requirements.txt` |
| Full auto | `--full-auto` | Scan + fix safe + deps + report |
| Silent | `--silent` | Output solo su file JSON, niente terminale |

### 6.2 Integrazione con `speace_status_monitor.py`

Aggiungere nel metodo `run_heartbeat()` di `speace_status_monitor.py`:

```python
def run_heartbeat(self):
    ...
    # Auto-Revision check
    if self._should_run_revision():
        revision = subprocess.run(
            [sys.executable, "scripts/speace_auto_revision.py", "--scan-only", "--silent"],
            capture_output=True, text=True
        )
        report = json.loads(revision.stdout)
        status["auto_revision"] = {
            "last_run": datetime.now().isoformat(),
            "issues_found": sum(p["issues_found"] for p in report["phases"].values()),
            "safe_fixes_applied": report.get("safe_fixes_applied", 0)
        }
```

### 6.3 Cron / Schedule

Esempio di scheduling con la libreria `schedule` (già in `requirements.txt`):

```python
import schedule
import time

schedule.every().day.at("06:00").do(run_auto_revision)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## 7. Metriche di Successo

| Metrica | Target | Misurazione |
|---------|--------|-------------|
| **Import Resolution Rate** | 100% | `resolved_imports / total_imports` |
| **Dependency Coverage** | 100% | `listed_deps / used_deps` |
| **Alignment Score Consistency** | 1 | Numero di valori diversi di alignment score nel repo |
| **Fitness Formula Sync** | True | Pesi in YAML == pesi in codice |
| **Structural Drift** | 0 | File/directory mancanti rispetto alla documentazione |
| **Auto-Fix Success Rate** | >95% | Fix applicati senza errore / fix tentati |
| **Proposal Approval Rate** | >80% | Proposte umane approvate / proposte generate |
| **Revision Cycle Time** | <60s | Tempo di esecuzione completo dello script |

---

## 8. Appendice A – Mappa delle Dipendenze tra Moduli

```
SPEACE-main.py
├── safe-proactive/ ...................... (PROPOSALS.md, auto-rules.json)
│   └── SafeProactive (namespace doc v1.2)
├── SPEACE_Cortex/
│   ├── smfoi-kernel/smfoi_v0_3.py ....... (fitness hardcoded vs YAML)
│   ├── learning_core/online_learner.py .. (river, numpy)
│   ├── memory/semantic_store.py ......... (chromadb, sentence-transformers)
│   ├── agente_organismo/ ............... (sensori simulati)
│   └── adaptive_consciousness/ ........... (numpy)
├── MultiFramework/
│   └── anythingllm/ ...................... (flask, stubs)
├── scientific-team/
│   └── agents/base_agent.py .............. (anthropic)
├── DigitalDNA/
│   ├── genome.yaml ....................... (fonte di verità strutturale)
│   ├── epigenome.yaml .................... (fonte di verità alignment)
│   ├── fitness_function.yaml ............. (fonte di verità fitness)
│   └── mutation_rules.yaml ............... (fonte di verità evoluzione)
└── requirements.txt ........................ (target di allineamento)
```

---

## 9. Appendice B – Checklist Operativa

### Prima Esecuzione
- [ ] Verificare che `python scripts/speace_auto_revision.py --scan-only` completi senza errori
- [ ] Controllare `speace_auto_revision_report.json` per il numero di issue
- [ ] Revisionare `PROPOSALS_AUTO_REVISION.md` per le proposte umane

### Esecuzione Periodica (giornaliera)
- [ ] Lanciare con `--apply-deps` se nuove dipendenze rilevate
- [ ] Verificare che `alignment_score` sia consistente in tutti i moduli
- [ ] Controllare che `requirements.txt` sia completo

### Post-Correzione
- [ ] Eseguire `python SPEACE-main.py --once` per validare l'entry point
- [ ] Eseguire `python tests/smoke_test.py` per validare la struttura
- [ ] Verificare `docker-compose.yml` se modificato

---

**Documento creato:** 22 aprile 2026  
**Ultimo aggiornamento:** 22 aprile 2026  
**Stato:** Pronto per implementazione  
**Prossima revisione:** 23 aprile 2026
