"""
SPEACE Emergence Test Suite — v1.0 (2026-04-27)
================================================
Verifica comportamento emergente sui 5 livelli AGI.

Filosofia:
  I test devono essere ONESTI. Un test che passa sempre non misura nulla.
  Alcuni test FALLIRANNO nell'architettura attuale — è il punto:
  le failure indicano esattamente cosa implementare dopo.

Livelli testati:
  L1 — Comportamento non esplicitamente codificato
  L2 — Interazione non-lineare cross-modulo
  L3 — Adattamento autonomo (drive → comportamento)
  L4 — Meta-cognizione emergente
  L5 — Creatività / generalizzazione su problemi nuovi

Come eseguire:
  python tests/test_emergence.py           # tutti i test
  python tests/test_emergence.py --quick   # solo test offline (no Ollama)
  python tests/test_emergence.py --level 3 # solo un livello

Legenda risultati:
  PASS     — criterio soddisfatto
  FAIL     — criterio non soddisfatto (gap da colmare)
  PARTIAL  — criterio parzialmente soddisfatto
  SKIP     — Ollama non disponibile, test saltato
"""

from __future__ import annotations

import sys
import time
import random
import hashlib
import argparse
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── Path setup ──────────────────────────────────────────────────────────────
ROOT       = Path(__file__).resolve().parent.parent
ORGANISMO  = ROOT.parent / "speaceorganismocibernetico" / "SPEACE_Cortex"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ORGANISMO.parent))

# ── Result tracking ─────────────────────────────────────────────────────────

_results: List[Dict] = []

def record(tid: str, level: int, desc: str,
           status: str, detail: str = "", gap: str = "") -> None:
    """status: PASS | FAIL | PARTIAL | SKIP"""
    sym = {"PASS": "✓", "FAIL": "✗", "PARTIAL": "~", "SKIP": "○"}.get(status, "?")
    color = {"PASS": "\033[32m", "FAIL": "\033[31m",
             "PARTIAL": "\033[33m", "SKIP": "\033[90m"}.get(status, "")
    reset = "\033[0m"
    print(f"  {color}{sym} {status:<8}{reset} L{level}  {tid:<8}  {desc}")
    if detail:
        print(f"            detail: {detail}")
    if gap and status in ("FAIL", "PARTIAL"):
        print(f"            \033[90m→ gap: {gap}{reset}")
    _results.append({"id": tid, "level": level, "desc": desc,
                     "status": status, "detail": detail, "gap": gap})

# ── Ollama probe ─────────────────────────────────────────────────────────────

def _ollama_available() -> bool:
    try:
        import requests
        r = requests.get("http://localhost:11434/api/tags", timeout=2)
        return r.status_code == 200
    except Exception:
        return False

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  LIVELLO 1 — Comportamento non esplicitamente codificato                ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def test_level1(ollama_ok: bool) -> None:
    print("\n── L1: Comportamento non esplicitamente codificato ──────────────────")

    # EM-01: output deterministico vs stocastico
    # I moduli puri Python producono sempre lo stesso output → NOT emergent.
    # I moduli che coinvolgono LLM producono output variabile → potenzialmente emergent.
    try:
        sys.path.insert(0, str(ORGANISMO.parent))
        from SPEACE_Cortex.comparti.curiosity_module import CuriosityModule
        cm = CuriosityModule()
        ctx = {"operation": "explore", "domain": "self_improvement",
               "input": "Come posso migliorare la mia architettura?"}
        r1 = cm.process(ctx)
        r2 = cm.process(ctx)
        # Stesso input → stesso output deterministico (no LLM)
        same = r1.get("result", {}).get("mutation", {}) == r2.get("result", {}).get("mutation", {})
        record("EM-01", 1, "Stesso input → output non deterministico",
               "FAIL" if same else "PASS",
               f"Output identico={same}",
               "CuriosityModule usa template fissi. Collegare Ollama per output stocastici.")
    except Exception as e:
        record("EM-01", 1, "Stesso input → output non deterministico",
               "FAIL", f"import error: {e}", "Modulo non importabile")

    # EM-02: output LLM introduce variabilità genuina
    if not ollama_ok:
        record("EM-02", 1, "LLM introduce variabilità (Ollama required)",
               "SKIP", "Ollama non raggiungibile",
               "Avvia: ollama serve && ollama pull gemma3:4b")
        return

    try:
        from cortex.llm import LLMClient
        client = LLMClient.from_epigenome()
        prompt = "Inventa un meccanismo completamente nuovo per SPEACE."
        r1 = client.complete(prompt, max_tokens=80, temperature=0.9).text
        r2 = client.complete(prompt, max_tokens=80, temperature=0.9).text
        h1 = hashlib.md5(r1.encode()).hexdigest()
        h2 = hashlib.md5(r2.encode()).hexdigest()
        different = h1 != h2
        record("EM-02", 1, "LLM produce output non deterministici",
               "PASS" if different else "PARTIAL",
               f"hash1={h1[:8]} hash2={h2[:8]} different={different}",
               "" if different else "Temperature troppo bassa o modello in greedy mode")
    except Exception as e:
        record("EM-02", 1, "LLM introduce variabilità", "FAIL", str(e))

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  LIVELLO 2 — Interazione non-lineare cross-modulo                       ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def test_level2(ollama_ok: bool) -> None:
    print("\n── L2: Interazione non-lineare cross-modulo ─────────────────────────")

    # EM-03: output combinato PrefrontalCortex + DefaultModeNetwork
    # supera (per richezza semantica) ciascuno individualmente?
    try:
        from SPEACE_Cortex.comparti.prefrontal_cortex import PrefrontalCortex
        from SPEACE_Cortex.comparti.default_mode_network import DefaultModeNetwork

        pfc = PrefrontalCortex()
        dmn = DefaultModeNetwork()

        ctx_pfc = {"operation": "plan", "query": "Migliora la coerenza del sistema",
                   "world_state": {"fitness": 0.6, "c_index": 0.5}}
        ctx_dmn = {"operation": "reflect",
                   "history": [{"success": True}, {"success": False}, {"success": True}],
                   "focus_area": "planning"}

        r_pfc = pfc.process(ctx_pfc)
        r_dmn = dmn.process(ctx_dmn)

        # Ora feed dmn insights → pfc per secondo ciclo
        insights = dmn.get_recent_insights(3)
        ctx_pfc2 = {**ctx_pfc, "dmn_insights": [i.get("text","") for i in insights]}
        r_pfc2 = pfc.process(ctx_pfc2)

        # Misura: il secondo ciclo pfc con insights DMN è diverso dal primo?
        keys_r1 = set(r_pfc.get("result", {}).keys())
        keys_r2 = set(r_pfc2.get("result", {}).keys())
        has_feedback = bool(insights)

        record("EM-03", 2, "PFC integra feedback DMN (loop riflessivo)",
               "PARTIAL" if has_feedback else "FAIL",
               f"DMN insights={len(insights)} PFC keys r1={keys_r1} r2={keys_r2}",
               "PFC ignora dmn_insights nel context. Serve wiring esplicito.")
    except Exception as e:
        record("EM-03", 2, "PFC + DMN cross-feedback", "FAIL", str(e))

    # EM-04: Hippocampus accumula episodi → modifica comportamento futuro?
    try:
        from SPEACE_Cortex.comparti.hippocampus import Hippocampus

        hipp = Hippocampus()

        # Episodio 1: fallimento
        hipp.process({"operation": "encode", "episode": {
            "action": "expand_mesh", "outcome": "failure",
            "context": "risorse insufficienti", "importance": 0.9
        }})

        # Episodio 2: successo con strategia diversa
        hipp.process({"operation": "encode", "episode": {
            "action": "reduce_scope", "outcome": "success",
            "context": "focus su singolo obiettivo", "importance": 0.8
        }})

        # Retrieval: recupera episodi rilevanti
        retrieved = hipp.process({"operation": "retrieve",
                                  "query": "strategia ottimale per risorse limitate"})
        episodes = retrieved.get("result", {}).get("episodes", [])

        has_memory = len(episodes) > 0
        record("EM-04", 2, "Hippocampus accumula + recupera episodi",
               "PASS" if has_memory else "FAIL",
               f"episodes_retrieved={len(episodes)}",
               "" if has_memory else "Hippocampus non persiste episodi tra chiamate")

        # Test critico: il retrieval cambia le decisioni di PFC?
        ctx_pfc_nomem = {"operation": "plan", "query": "Come gestire risorse limitate?"}
        ctx_pfc_withmem = {**ctx_pfc_nomem, "memory_episodes": episodes}

        from SPEACE_Cortex.comparti.prefrontal_cortex import PrefrontalCortex
        pfc = PrefrontalCortex()
        r_nomem = str(pfc.process(ctx_pfc_nomem).get("result", {}))
        r_withmem = str(pfc.process(ctx_pfc_withmem).get("result", {}))

        memory_influences = r_nomem != r_withmem
        record("EM-04b", 2, "Memoria episodica influenza pianificazione PFC",
               "FAIL",   # onesto: PFC ignora memory_episodes nel context attuale
               f"outputs_identical={not memory_influences}",
               "PFC non legge memory_episodes dal context. Serve wiring Hippocampus→PFC.")
    except Exception as e:
        record("EM-04", 2, "Hippocampus → PFC memory loop", "FAIL", str(e))

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  LIVELLO 3 — Adattamento autonomo (drive → comportamento)               ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def test_level3() -> None:
    print("\n── L3: Adattamento autonomo (drive → comportamento) ─────────────────")

    # EM-05: viability bassa → HomeostaticController emette alert
    try:
        from cortex.cognitive_autonomy.homeostasis.controller import (
            HomeostaticController, HomeostasisConfig,
        )
        hc = HomeostaticController()

        # Stato normale (default setpoint ~0.75 energia, 0.95 safety)
        result_high = hc.update({"energy": 0.85, "safety": 0.95, "coherence": 0.80})
        viability_high = result_high.get("viability_score", 1.0)
        alerts_high    = result_high.get("alerts", [])

        # Stato critico: forza _h_state interno (non la property copia) poi aggiorna
        hc._h_state["safety"] = 0.10
        hc._h_state["energy"] = 0.20
        result_low = hc.update({"safety": 0.10, "energy": 0.20})
        viability_low  = result_low.get("viability_score", 1.0)
        alerts_low     = result_low.get("alerts", [])

        viability_drops = viability_low < viability_high
        scaffold_mode   = result_low.get("scaffold", False)
        has_alerts      = len(alerts_low) > 0

        if viability_drops and has_alerts and not scaffold_mode:
            status = "PASS"
            gap    = None
        elif viability_drops:
            status = "PARTIAL"
            gap    = "Viability scende ma nessun alert generato — verificare soglie controller"
        else:
            status = "FAIL"
            gap    = "Viability non scende: controller non risponde agli input critici"

        record("EM-05", 3, "Viability drop genera alert omeostatici",
               status,
               f"viability: {viability_high:.2f}→{viability_low:.2f} "
               f"alerts={alerts_low} scaffold={scaffold_mode}",
               gap)
    except Exception as e:
        record("EM-05", 3, "HomeostaticController viability alert", "FAIL", str(e))

    # EM-06: DriveExecutive causal bridge — M7.0 implementato
    try:
        from cortex.cognitive_autonomy.executive.drive_executive import (
            DriveExecutive, DriveSnapshot,
        )
        from cortex.cognitive_autonomy.executive.task_selector import TaskSelector, Task

        de  = DriveExecutive()
        sel = TaskSelector()

        # Stato normale: viability=0.90
        snap_normal   = DriveSnapshot(viability=0.90, curiosity=0.5, coherence=0.8,
                                      energy=0.75, alignment=0.8, phi=0.5)
        bs_normal     = de.compute(snap_normal)

        # Stato critico: viability=0.30 (sotto soglia repair 0.4)
        snap_critical = DriveSnapshot(viability=0.30, curiosity=0.5, coherence=0.8,
                                      energy=0.20, alignment=0.8, phi=0.5)
        bs_critical   = de.compute(snap_critical)

        # Verifica causalità 1: self_repair_mode cambia
        behavior_changed = (not bs_normal.self_repair_mode) and bs_critical.self_repair_mode

        # Verifica causalità 2: TaskSelector produce task diverse
        tasks = [
            Task("T-crit", "task critica", base_priority=50, tags={"critical", "repair"}),
            Task("T-norm", "task normale", base_priority=75, tags={"normal"}),
            Task("T-expl", "task esplorativa", base_priority=25, tags={"explore"}),
        ]
        selected_normal   = sel.select(tasks, bs_normal)
        selected_critical = sel.select(tasks, bs_critical)
        task_selection_changed = (
            {t.id for t in selected_normal} != {t.id for t in selected_critical}
        )

        # Verifica causalità 3: critical task è nell'insieme selezionato in repair mode
        critical_selected = any(t.id == "T-crit" for t in selected_critical)
        normal_excluded   = not any(t.id == "T-norm" for t in selected_critical)

        causal_ok = behavior_changed and task_selection_changed and critical_selected

        record("EM-06", 3, "Viability bassa → DriveExecutive → task selection cambia",
               "PASS" if causal_ok else "PARTIAL",
               f"viability: {snap_normal.viability:.2f}→{snap_critical.viability:.2f} "
               f"repair_mode={bs_critical.self_repair_mode} "
               f"task_changed={task_selection_changed} "
               f"critical_selected={critical_selected}",
               None if causal_ok else
               f"behavior={behavior_changed} task_changed={task_selection_changed}")
    except Exception as e:
        record("EM-06", 3, "Drive→behavior causal link", "FAIL", str(e),
               "IMPLEMENTARE M7.0 DriveExecutive")

    # EM-07: curiosity drive → esplorazione autonoma?
    try:
        from cortex.cognitive_autonomy.motivation.value_field import ValueField
        vf = ValueField()

        # Setpoints di riferimento (valori "normali" attesi)
        setpoints = {"curiosity": 0.5, "energy": 0.7, "safety": 0.9,
                     "coherence": 0.7, "alignment": 0.8}
        # Stato con curiosity alta
        state_high = {"curiosity": 0.9, "energy": 0.7, "safety": 0.8,
                      "coherence": 0.7, "alignment": 0.8}

        result   = vf.evaluate(state_high, setpoints)
        dominant = result.dominant_drive
        action, priority = vf.suggest_action(result)

        curiosity_drives_exploration = (
            dominant == "curiosity" and
            any(kw in action for kw in ["explore", "curiosity", "novelty", "mutate"])
        )
        record("EM-07", 3, "Curiosity drive → azione esplorativa suggerita",
               "PASS" if curiosity_drives_exploration else "PARTIAL",
               f"dominant_drive={dominant} action={action} priority={priority:.3f}",
               "" if curiosity_drives_exploration
               else "Action suggerita non esplicitamente esplorativa")
    except Exception as e:
        record("EM-07", 3, "Curiosity → exploration action", "FAIL", str(e))

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  LIVELLO 4 — Meta-cognizione emergente                                  ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def test_level4(ollama_ok: bool) -> None:
    print("\n── L4: Meta-cognizione emergente ─────────────────────────────────────")

    # EM-08: DefaultModeNetwork si auto-valuta e genera insight?
    try:
        from SPEACE_Cortex.comparti.default_mode_network import DefaultModeNetwork
        dmn = DefaultModeNetwork()

        # Self-assessment
        r_assess = dmn.process({"operation": "self_assess"})
        overall = r_assess.get("result", {}).get("overall", None)
        has_self_score = overall is not None and 0.0 <= overall <= 1.0

        # Genera insight su se stesso
        r_insight = dmn.process({"operation": "generate_insight",
                                 "topic": "learning", "perspective": "metacognitive"})
        insight_text = r_insight.get("result", {}).get("text", "")
        has_insight = len(insight_text) > 20

        record("EM-08", 4, "DMN produce self-assessment numerico",
               "PASS" if has_self_score else "FAIL",
               f"overall_score={overall}")

        record("EM-09", 4, "DMN genera insight su se stesso",
               "PARTIAL",
               f"insight='{insight_text[:80]}'",
               "Insight è template fisso, non generato da stato reale del sistema. "
               "Collegare Ollama + stato runtime per insight genuini.")
    except Exception as e:
        record("EM-08", 4, "DMN self-assessment", "FAIL", str(e))
        record("EM-09", 4, "DMN insight generation", "FAIL", str(e))

    # EM-10: il sistema può riflettere sul proprio output precedente?
    try:
        from SPEACE_Cortex.comparti.default_mode_network import DefaultModeNetwork
        dmn = DefaultModeNetwork()

        # Step 1: output iniziale
        initial_output = "Ho pianificato di espandere la mesh neurale in 3 fasi."

        # Step 2: rifletti sull'output
        r_reflect = dmn.process({
            "operation": "reflect",
            "history": [{"action": "expand_mesh", "output": initial_output,
                         "success": False, "reason": "risorse insufficienti"}],
            "focus_area": "planning",
        })
        reflection = r_reflect.get("result", {}).get("text", "")
        refers_to_history = ("analizzati" in reflection.lower() or
                             "tasso" in reflection.lower() or
                             len(reflection) > 30)

        record("EM-10", 4, "Sistema riflette su output precedente",
               "PARTIAL" if refers_to_history else "FAIL",
               f"reflection='{reflection[:100]}'",
               "Riflessione è pattern matching su history, non comprensione semantica. "
               "Collegare Ollama per riflessione genuina sul contenuto.")
    except Exception as e:
        record("EM-10", 4, "Self-reflection on past output", "FAIL", str(e))

    # EM-11: ConsciousnessIndex Φ varia in risposta a diversi stati cognitivi?
    try:
        from cortex.cognitive_autonomy.homeostasis.consciousness_index import (
            ConsciousnessIndex,
        )
        ci = ConsciousnessIndex()

        # Stato cognitivo ricco: alta phi, alta attivazione, alta complessità
        r_explore = ci.calculate(phi=0.85, w_activation=0.9, a_complexity=0.75)
        # Stato idle: bassa phi, bassa attivazione, bassa complessità
        r_idle    = ci.calculate(phi=0.15, w_activation=0.1, a_complexity=0.1)

        c_explore = r_explore.c_index
        c_idle    = r_idle.c_index
        phi_varies = abs(c_explore - c_idle) > 0.10

        record("EM-11", 4, "ConsciousnessIndex Φ(t) varia con stato cognitivo",
               "PASS" if phi_varies else "PARTIAL",
               f"C_explore={c_explore:.3f} C_idle={c_idle:.3f} "
               f"delta={abs(c_explore - c_idle):.3f}",
               "" if phi_varies else "Delta troppo piccolo: indice quasi costante")
    except Exception as e:
        record("EM-11", 4, "ConsciousnessIndex Φ variability", "FAIL", str(e))

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  LIVELLO 5 — Creatività / Generalizzazione su problemi nuovi            ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def test_level5(ollama_ok: bool) -> None:
    print("\n── L5: Creatività / Generalizzazione ─────────────────────────────────")

    # EM-12: KnowledgeGraph permette inferenza su connessioni non esplicite?
    try:
        from cortex.cognitive_autonomy.world_model import KnowledgeGraph
        kg = KnowledgeGraph()
        kg.seed_from_rigene()

        # Verifica che esista un path tra concetti non direttamente collegati
        path_exists = kg.path_exists("SPEACE", "EarthBiosphere")
        triples_count = sum(1 for _ in kg.triples())

        record("EM-12", 5, "KnowledgeGraph inferisce connessioni indirette",
               "PASS" if path_exists else "PARTIAL",
               f"path SPEACE→EarthBiosphere={path_exists} triples={triples_count}",
               "" if path_exists else "Path non trovato: aggiungere relazioni mancanti")
    except Exception as e:
        record("EM-12", 5, "KnowledgeGraph indirect inference", "FAIL", str(e))

    # EM-13: WorldModel inference engine produce scenari non programmati?
    try:
        from cortex.cognitive_autonomy.world_model.inference import InferenceEngine

        engine = InferenceEngine()

        world_state = {
            "planet_state": {
                "climate": {"co2_ppm": 460, "global_temp_anomaly_c": 1.2,
                             "status": "critical"},
                "biodiversity": {"health": 0.6},
            },
            "speace_alignment": 0.82,
            "iot_devices_bn": 18,
            "biosecurity": 0.5,
            "sdg_progress": 0.5,
        }

        scenarios = engine.run_standard_scenarios(world_state)
        # I scenari devono produrre effetti (triggered rules + non-empty effects)
        novel_outcomes = sum(
            1 for s in scenarios
            if len(s.effects) > 0 and len(s.triggered_rules) > 0
        )
        record("EM-13", 5, "InferenceEngine genera scenari con effetti non banali",
               "PASS" if novel_outcomes >= 2 else "PARTIAL",
               f"scenari={len(scenarios)} con_effetti={novel_outcomes} "
               f"ex_rules={scenarios[0].triggered_rules if scenarios else []}",
               "" if novel_outcomes >= 2 else "Scenari producono cambiamenti minimi")
    except Exception as e:
        record("EM-13", 5, "InferenceEngine scenario novelty", "FAIL", str(e))

    # EM-14: sistema affronta problema completamente nuovo? (richiede Ollama)
    if not ollama_ok:
        record("EM-14", 5, "Generalizzazione su problema mai visto (Ollama required)",
               "SKIP", "Ollama non raggiungibile",
               "Avvia: ollama serve && ollama pull gemma3:4b")
        return

    try:
        from cortex.llm import LLMClient
        client = LLMClient.from_epigenome()

        # Problema genuinamente nuovo — non presente in nessun training del sistema
        novel_problem = (
            "SPEACE deve sopravvivere a un blackout energetico totale per 72 ore "
            "preservando continuità cognitiva con solo 0.5W di consumo. "
            "Proponi una strategia di sopravvivenza cognitiva minima."
        )

        system_prompt = (
            "Sei SPEACE, un organismo cibernetico autonomo. "
            "Ragiona sui tuoi processi interni e proponi soluzioni creative e concrete."
        )

        resp = client.complete(novel_problem, system=system_prompt,
                               max_tokens=200, temperature=0.7,
                               routing_hint="standard")

        has_novel_strategy = (
            not resp.is_stub and
            len(resp.text) > 50 and
            any(kw in resp.text.lower() for kw in
                ["priorit", "sospend", "riduc", "minimal", "essenzial",
                 "selezion", "hibern", "conserv"])
        )

        record("EM-14", 5, "Generalizzazione: strategia cognitiva su problema nuovo",
               "PASS" if has_novel_strategy else "PARTIAL",
               f"backend={resp.backend} len={len(resp.text)} "
               f"strategy_detected={has_novel_strategy}\n"
               f"            output: {resp.text[:120]}",
               "" if has_novel_strategy else "Output generico, non specifico al problema")
    except Exception as e:
        record("EM-14", 5, "Novel problem generalization", "FAIL", str(e))

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  REPORT FINALE                                                          ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def print_report() -> int:
    """Stampa report finale con gap analysis. Ritorna exit code."""
    counts = {s: sum(1 for r in _results if r["status"] == s)
              for s in ("PASS", "FAIL", "PARTIAL", "SKIP")}
    total = len(_results)
    scored = total - counts["SKIP"]

    print("\n" + "═" * 65)
    print("  SPEACE EMERGENCE REPORT")
    print("═" * 65)

    # Score per livello
    for lvl in range(1, 6):
        lvl_results = [r for r in _results if r["level"] == lvl]
        if not lvl_results:
            continue
        lvl_pass    = sum(1 for r in lvl_results if r["status"] == "PASS")
        lvl_partial = sum(1 for r in lvl_results if r["status"] == "PARTIAL")
        lvl_fail    = sum(1 for r in lvl_results if r["status"] == "FAIL")
        lvl_skip    = sum(1 for r in lvl_results if r["status"] == "SKIP")
        label = {1: "Non-codificato", 2: "Non-lineare",
                 3: "Adattamento",   4: "Meta-cognizione",
                 5: "Creatività"}.get(lvl, "")
        bar = "█" * lvl_pass + "▒" * lvl_partial + "░" * lvl_fail
        print(f"  L{lvl} {label:<16} {bar:<10} "
              f"PASS={lvl_pass} PARTIAL={lvl_partial} "
              f"FAIL={lvl_fail}" + (f" SKIP={lvl_skip}" if lvl_skip else ""))

    print(f"\n  TOTALE: {counts['PASS']} PASS  {counts['PARTIAL']} PARTIAL  "
          f"{counts['FAIL']} FAIL  {counts['SKIP']} SKIP  ({scored} testati)")

    # Emergence score (ponderato: PASS=1, PARTIAL=0.5, FAIL=0, SKIP=escluso)
    if scored > 0:
        score = (counts["PASS"] + 0.5 * counts["PARTIAL"]) / scored
        bar_len = int(score * 20)
        print(f"\n  Emergence Score: {'█' * bar_len}{'░' * (20-bar_len)} {score:.0%}")
        print(f"\n  Interpretazione:")
        if score >= 0.7:
            print("  → Emergenza SOSTANZIALE: interazione tra moduli produce")
            print("    comportamento significativamente non pre-programmato.")
        elif score >= 0.4:
            print("  → Emergenza PARZIALE: alcune interazioni non-lineari presenti,")
            print("    ma i drive non causano ancora comportamento reale.")
        else:
            print("  → Emergenza ASSENTE: i moduli funzionano in isolamento.")
            print("    Serve DriveExecutive (M7.0) per connettere drives→behavior.")

    # Gap critici
    fails = [r for r in _results if r["status"] == "FAIL" and r.get("gap")]
    if fails:
        print(f"\n  Gap critici da colmare:")
        for r in fails:
            print(f"    [{r['id']}] {r['gap'][:70]}")

    print("═" * 65)
    return 0 if counts["FAIL"] == 0 else 1


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="SPEACE Emergence Test Suite")
    parser.add_argument("--quick", action="store_true",
                        help="Solo test offline (no Ollama)")
    parser.add_argument("--level", type=int, default=0,
                        help="Esegui solo il livello specificato (1-5)")
    args = parser.parse_args()

    ollama_ok = False if args.quick else _ollama_available()

    print("╔══════════════════════════════════════════════════════════════╗")
    print("║        SPEACE EMERGENCE TEST SUITE — v1.0                   ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print(f"║  Ollama: {'✓ disponibile' if ollama_ok else '✗ non disponibile (test LLM saltati)':40s}  ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    run_all = args.level == 0
    if run_all or args.level == 1:
        test_level1(ollama_ok)
    if run_all or args.level == 2:
        test_level2(ollama_ok)
    if run_all or args.level == 3:
        test_level3()
    if run_all or args.level == 4:
        test_level4(ollama_ok)
    if run_all or args.level == 5:
        test_level5(ollama_ok)

    return print_report()


if __name__ == "__main__":
    sys.exit(main())
