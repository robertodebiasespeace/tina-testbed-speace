# Istruzioni Operative per SPEACE Auto-Pilot

Questo documento guida l'Auto-Pilot Bridge (`scripts/speace_autopilot.py`) nel generare prompt migliorativi per Claude Code, e guida Claude Code stesso sul comportamento da tenere quando riceve i prompt automatici.

---

## Principi Generali

1. **Priorità ai task critici**: Task con stato `Non Iniziato` + priorità `Critica` vengono sempre proposti per primi.
2. **Operazioni read-only approvate**: Lettura file, analisi codice, test, grep, glob sono operazioni sicure e possono essere eseguite senza conferma umana.
3. **Operazioni distruttive proibite in autonomia**: `rm`, `git push --force`, drop database, cancellazione branch, modifiche a `.git/`, file di sistema richiedono sempre proposta in `safe-proactive/` e attesa approvazione umana.
4. **Allineamento continuo**: Ogni ciclo deve verificare la coerenza tra `DigitalDNA/genome.yaml`, `epigenome.yaml` e i valori hardcoded nel codice.
5. **Memoria persistente**: Se rilevi nuovi pattern, aggiorna la memoria del progetto in `.claude/projects/.../memory/`.

---

## Aree di Intervento Prioritarie

### 1. DigitalDNA
- Verifica che `genome.yaml`, `epigenome.yaml`, `fitness_function.yaml` siano sintatticamente validi.
- Controlla che i pesi della fitness function nel codice (es. SMFOI) combacino con il YAML.
- Se lo `alignment_score` è inferiore a 70, genera task per migliorarlo.

### 2. Neural Engine
- Monitora i neuroni con `fitness_score < 0.5`.
- Se ci sono neuroni in stato `ERROR` da più di 3 cicli, proponi pruning o debug.
- Verifica che il grafo abbia almeno 7 neuroni e 10 sinapsi attive.

### 3. SafeProactive
- Leggi `safe-proactive/PROPOSALS.md` per proposte pending.
- Non approvare proposte `high_risk` o `regulatory` senza review umana.
- Mantieni il WAL (Write-Ahead Log) coerente.

### 4. Scientific Team
- Se i sensori ambiente rilevano anomalie, attiva il Team Scientifico per briefing.
- Genera `Daily Brief` solo se ci sono nuovi dati dall'ultimo ciclo.

### 5. Multi-Framework
- Verifica che i wrapper AGPT e Hermes siano importabili senza errori.
- Se AnythingLLM è offline, proponi restart o diagnosi.

---

## Comportamento di Sicurezza (vincoli assoluti)

- **NON** confermare prompt di permesso su operazioni distruttive.
- **NON** modificare file al di fuori di `C:\Users\rober\Desktop\ProgettoCode\speaceorganismocibernetico`.
- **NON** eseguire comandi di rete verso host non noti (es. `curl` verso URL sospetti).
- **NON** condividere API key, token, o credenziali in nessun log o file.
- **NON** installare pacchetti PyPI senza verificare il nome e la reputazione.

---

## Flusso Operativo di un Ciclo Auto-Pilot

```
1. Scansiona docs/ per documenti rilevanti
2. Legge speace_status.json e speace_auto_revision_report.json
3. Estrae task pending dal tracker
4. Compone prompt strutturato
5. Invia prompt a Claude Code tramite terminale
6. Claude Code esegue analisi e operazioni safe
7. Se necessario, genera proposte in safe-proactive/
8. Aggiorna stato e memoria
```

---

## Aggiornamento di questo Documento

Quando il comportamento dell'Auto-Pilot deve cambiare (nuove priorità, nuove aree, nuovi vincoli), modifica questo file. L'Auto-Pilot lo legge automaticamente ad ogni ciclo e ne include il contenuto nel prompt inviato a Claude Code.

---

**Versione:** 1.0  
**Data:** 22 aprile 2026  
**Autore:** SPEACE Cortex  
**Allineamento:** Fase 1 → Fase 2 Transition
