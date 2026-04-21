"""
SPEACE – Entry Point Principale
SuPer Entità Autonoma Cibernetica Evolutiva

Avvia il sistema SPEACE completo:
- Inizializza SafeProactive (snapshot iniziale)
- Attiva World Model
- Esegue cicli SMFOI-KERNEL
- Coordina Cortex e Team Scientifico

Versione: 1.0 | 2026-04-17
Uso: python SPEACE-main.py [--once] [--cycles=N] [--team] [--neural]
Note: --neural attiva il Neural Engine per automazione processi cerebrali
"""

import sys
import os
import json
import argparse
import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

BANNER = """
╔══════════════════════════════════════════════════════════╗
║   SPEACE  –  SuPer Entità Autonoma Cibernetica Evolutiva ║
║   Versione 1.0 | Fase 1 – Embrionale                    ║
║   Fondatore: Roberto De Biase (Rigene Project)           ║
╚══════════════════════════════════════════════════════════╝
"""


def check_dependencies():
    """Verifica che le dipendenze Python siano installate."""
    missing = []
    deps = ["yaml", "requests", "psutil"]
    for dep in deps:
        try:
            __import__(dep)
        except ImportError:
            missing.append(dep)
    if missing:
        print(f"[SPEACE] ⚠️  Dipendenze mancanti: {', '.join(missing)}")
        print(f"[SPEACE] Installa con: pip install {' '.join(missing)}")
        print("[SPEACE] oppure esegui: setup.bat")
        return False
    return True


def initialize_system():
    """Inizializza il sistema SPEACE al primo avvio."""
    print("[SPEACE] Inizializzazione sistema...")

    # Crea stato iniziale se assente
    state_file = ROOT_DIR / "state.json"
    if not state_file.exists():
        state = {
            "version": "1.0",
            "phase": 1,
            "created": datetime.datetime.now().isoformat(),
            "cycles": [],
            "last_fitness": 0.0,
            "last_cycle": None,
            "last_run": None,
        }
        state_file.write_text(json.dumps(state, indent=2))
        print("[SPEACE] ✅ state.json creato")

    # Crea MEMORY.md se assente
    memory_file = ROOT_DIR / "memory" / "MEMORY.md"
    if not memory_file.exists():
        memory_file.write_text(
            "# SPEACE Memory Index\n\n"
            "Indice della memoria persistente di SPEACE.\n\n"
            f"Creato: {datetime.datetime.now().isoformat()}\n\n"
        )
        print("[SPEACE] ✅ MEMORY.md creato")


def run_speace(cycles: int = 1, run_team: bool = False, continuous: bool = False, run_neural: bool = False):
    """Esegue il sistema SPEACE."""

    print(BANNER)
    print(f"[SPEACE] Avvio {datetime.datetime.now().isoformat()}")
    print(f"[SPEACE] Modalità: {'continua' if continuous else f'{cycles} ciclo/i'}")
    print(f"[SPEACE] Neural Engine: {'Attivo' if run_neural else 'Disattivo'}")

    if not check_dependencies():
        sys.exit(1)

    initialize_system()

    # Importa moduli SPEACE
    try:
        from safeproactive.safeproactive import SafeProactive, RiskLevel
        from cortex.SMFOI_v3 import SMFOIKernel
        from cortex.world_model import WorldModel
        from cortex.comparti.default_mode_network import DefaultModeNetwork
    except ImportError as e:
        print(f"[SPEACE] Errore import moduli: {e}")
        print("[SPEACE] Verifica che tutti i file siano presenti e le dipendenze installate.")
        sys.exit(1)

    # Importa Neural Engine se richiesto
    neural_engine = None
    if run_neural:
        try:
            from neural_engine.neural_main import SPEACENeuralEngine
            print("\n[SPEACE] ▶ Inizializzazione Neural Engine...")
            neural_engine = SPEACENeuralEngine()
            neural_engine.initialize()
            print("[SPEACE] ✅ Neural Engine attivo")
        except ImportError as e:
            print(f"[SPEACE] ⚠️  Neural Engine non disponibile: {e}")

    # 1. Inizializza SafeProactive e snapshot
    print("\n[SPEACE] ▶ Inizializzazione SafeProactive...")
    sp = SafeProactive()
    snap_id = sp.snapshot(label="startup")
    print(f"[SPEACE] ✅ Snapshot iniziale: {snap_id}")

    # 2. Inizializza World Model
    print("\n[SPEACE] ▶ Inizializzazione World Model...")
    wm = WorldModel()
    wm_summary = wm.get_summary()
    print(f"[SPEACE] ✅ World Model attivo | Nodi KG: {wm_summary['knowledge_nodes']}")

    # 3. Fetch obiettivi Rigene Project
    print("\n[SPEACE] ▶ Fetch obiettivi Rigene Project...")
    objs = wm.fetch_rigene_objectives()
    print(f"[SPEACE] ✅ {len(objs)} obiettivi caricati")

    # 4. Inizializza SMFOI-KERNEL
    print("\n[SPEACE] ▶ Inizializzazione SMFOI-KERNEL v0.3...")
    kernel = SMFOIKernel(agent_name="SPEACE-MAIN", recursion_level=1)
    dmn = DefaultModeNetwork()

    # Notifica avvio
    sp.propose(
        action_name="system_startup",
        description=f"Avvio sistema SPEACE v1.0 | {cycles} cicli pianificati",
        risk_level=RiskLevel.LOW,
        source_agent="speace-main"
    )

    # 5. Esegui cicli SMFOI
    cycle_history = []
    print(f"\n[SPEACE] ▶ Esecuzione {cycles} ciclo/i SMFOI...")

    if continuous:
        import time
        cycle_n = 0
        if neural_engine:
            neural_engine.start_background()
        try:
            while True:
                cycle_n += 1
                print(f"\n[SPEACE] {'='*40}")
                print(f"[SPEACE] CICLO CONTINUO #{cycle_n}")
                result = kernel.run_cycle()
                cycle_history.append(result)
                wm.update_speace_state(
                    last_cycle=result.get("cycle_id"),
                    fitness=result.get("outcome", {}).get("fitness_after", 0)
                )
                if neural_engine:
                    neural_status = neural_engine.get_status()
                    print(f"[SPEACE] Neural: {neural_status['cycle_count']} cicli | "
                          f"Balance: {neural_status['evolution']['balance']:.2f}")
                print(f"[SPEACE] Prossimo ciclo tra 60 secondi (Ctrl+C per fermare)...")
                time.sleep(60)
        finally:
            if neural_engine:
                neural_engine.stop_background()
    else:
        for i in range(cycles):
            print(f"\n[SPEACE] --- Ciclo {i+1}/{cycles} ---")
            result = kernel.run_cycle()
            cycle_history.append(result)
            wm.update_speace_state(
                last_cycle=result.get("cycle_id"),
                fitness=result.get("outcome", {}).get("fitness_after", 0)
            )

    # 6. Riflessione post-ciclo (Default Mode Network)
    print("\n[SPEACE] ▶ Auto-riflessione (Default Mode Network)...")
    reflection = dmn.reflect(cycle_history, wm)
    if reflection["insights"]:
        print("[SPEACE] 💡 Insights:")
        for insight in reflection["insights"]:
            print(f"  - {insight}")
    if reflection["suggestions"]:
        print("[SPEACE] 🔧 Suggerimenti:")
        for sug in reflection["suggestions"]:
            print(f"  - {sug}")

    # 7. Team Scientifico (opzionale)
    if run_team:
        print("\n[SPEACE] ▶ Avvio Team Scientifico...")
        try:
            sys.path.insert(0, str(ROOT_DIR / "scientific-team"))
            from orchestrator import ScientificTeamOrchestrator
            orchestrator = ScientificTeamOrchestrator()
            brief = orchestrator.run_daily_brief(wm_summary)
            print(f"\n[SPEACE] ✅ Daily Brief generato")
            print(brief[:500] + "...\n")
        except ImportError as e:
            print(f"[SPEACE] Team Scientifico non disponibile: {e}")
            print("[SPEACE] Assicurati che anthropic sia installato per usare il team.")

    # 8. Riepilogo finale
    final_fitness = cycle_history[-1].get("outcome", {}).get("fitness_after", 0) if cycle_history else 0
    print(f"\n{'='*60}")
    print(f"[SPEACE] ✅ SESSIONE COMPLETATA")
    print(f"[SPEACE] Cicli eseguiti: {len(cycle_history)}")
    print(f"[SPEACE] Fitness finale: {final_fitness:.4f}")
    print(f"[SPEACE] Proposte pending: vedere safeproactive/PROPOSALS.md")
    print(f"[SPEACE] Log disponibili in: logs/")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SPEACE – Entry Point")
    parser.add_argument("--once", action="store_true", help="Ciclo singolo")
    parser.add_argument("--cycles", type=int, default=2, help="Numero di cicli (default: 2)")
    parser.add_argument("--team", action="store_true", help="Attiva Team Scientifico")
    parser.add_argument("--continuous", action="store_true", help="Modalità continua (loop)")
    parser.add_argument("--neural", action="store_true", help="Attiva Neural Engine (background)")
    args = parser.parse_args()

    cycles = 1 if args.once else args.cycles
    run_speace(cycles=cycles, run_team=args.team, continuous=args.continuous, run_neural=args.neural)
