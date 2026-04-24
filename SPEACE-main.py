"""
SPEACE – Entry Point Principale v1.2
SuPer Entità Autonoma Cibernetica Evolutiva

Avvia il sistema SPEACE completo:
- Inizializza SafeProactive (snapshot iniziale)
- Attiva World Model
- Esegue cicli SMFOI-KERNEL
- Coordina Cortex e Team Scientifico

Versione: 1.2 | 2026-04-22
Uso: python SPEACE-main.py [--once] [--cycles=N] [--team] [--continuous]
"""

import sys
import os
import io

# Forza UTF-8 su Windows per evitare UnicodeEncodeError con simboli box-drawing
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

import json
import argparse
import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

BANNER = """
╔══════════════════════════════════════════════════════════╗
║   SPEACE  –  SuPer Entità Autonoma Cibernetica Evolutiva ║
║   Versione 1.2 | Fase 1 – Embrionale → Fase 2 Transition ║
║   Alignment: 67.3/100 | C-index: 0.683                   ║
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
        print("[SPEACE] oppure esegui: scripts/setup/setup.bat")
        return False
    return True


def initialize_system():
    """Inizializza il sistema SPEACE al primo avvio."""
    print("[SPEACE] Inizializzazione sistema...")

    # Crea stato iniziale se assente
    state_file = ROOT_DIR / "speace_status.json"
    if not state_file.exists():
        state = {
            "version": "1.2",
            "phase": "Fase 1 - Embrionale",
            "created": datetime.datetime.now().isoformat(),
            "cycles": [],
            "last_fitness": 0.7075,
            "last_cycle": None,
            "last_run": None,
        }
        state_file.write_text(json.dumps(state, indent=2))
        print("[SPEACE] ✅ speace_status.json creato")

    # Crea MEMORY.md se assente
    memory_file = ROOT_DIR / "memory" / "MEMORY.md"
    if not memory_file.exists():
        memory_file.parent.mkdir(parents=True, exist_ok=True)
        memory_file.write_text(
            "# SPEACE Memory Index\n\n"
            "Indice della memoria persistente di SPEACE.\n\n"
            f"Creato: {datetime.datetime.now().isoformat()}\n\n"
        )
        print("[SPEACE] ✅ MEMORY.md creato")


def run_speace(cycles: int = 1, run_team: bool = False, continuous: bool = False):
    """Esegue il sistema SPEACE."""

    print(BANNER)
    print(f"[SPEACE] Avvio {datetime.datetime.now().isoformat()}")
    print(f"[SPEACE] Modalità: {'continua' if continuous else f'{cycles} ciclo/i'}")

    if not check_dependencies():
        sys.exit(1)

    initialize_system()

    # Importa moduli SPEACE (gestione package con trattino nel nome)
    try:
        import importlib.util

        # safe-proactive (directory con trattino)
        sp_path = ROOT_DIR / "safe-proactive" / "safe_proactive.py"
        spec = importlib.util.spec_from_file_location("safe_proactive", str(sp_path))
        safe_proactive_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(safe_proactive_mod)
        SafeProactive = safe_proactive_mod.SafeProactive

        # smfoi-kernel (directory con trattino)
        smfoi_path = ROOT_DIR / "SPEACE_Cortex" / "smfoi-kernel" / "smfoi_v0_3.py"
        spec = importlib.util.spec_from_file_location("smfoi_v0_3", str(smfoi_path))
        smfoi_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(smfoi_mod)
        SMFOIKernel = smfoi_mod.SMFOIKernel

        from MultiFramework.anythingllm.query_interface import WorldModelQueryInterface
        print("[SPEACE] Moduli core importati")
    except ImportError as e:
        print(f"[SPEACE] ⚠️ Moduli opzionali non disponibili: {e}")
        print("[SPEACE] Esecuzione in modalità base...")
        SMFOIKernel = None
        SafeProactive = None
        WorldModelQueryInterface = None

    # 1. Inizializza SafeProactive
    print("\n[SPEACE] ▶ Inizializzazione SafeProactive...")
    try:
        sp = SafeProactive()
        print("[SPEACE] ✅ SafeProactive attivo")
    except Exception as e:
        print(f"[SPEACE] ⚠️ SafeProactive non disponibile: {e}")
        sp = None

    # 2. Inizializza World Model
    print("\n[SPEACE] ▶ Inizializzazione World Model...")
    try:
        wm = WorldModelQueryInterface()
        print("[SPEACE] ✅ World Model attivo")
    except Exception as e:
        print(f"[SPEACE] ⚠️ World Model non disponibile: {e}")
        wm = None

    # 3. Inizializza SMFOI-KERNEL
    print("\n[SPEACE] ▶ Inizializzazione SMFOI-KERNEL v0.3...")
    try:
        kernel = SMFOIKernel() if SMFOIKernel else None
        if kernel:
            print("[SPEACE] ✅ SMFOI-KERNEL pronto")
    except Exception as e:
        print(f"[SPEACE] ⚠️ SMFOI-KERNEL non disponibile: {e}")
        kernel = None

    # 3.5 Inizializza Neural Bridge (grafo computazionale)
    print("\n[SPEACE] ▶ Inizializzazione Neural Bridge...")
    neural_bridge = None
    try:
        from SPEACE_Cortex.neural_bridge import SPEACENeuralBridge
        neural_bridge = SPEACENeuralBridge(
            safe_proactive=sp,
            smfoi_kernel=kernel,
            world_model=wm,
        )
        neural_bridge.initialize()
        print("[SPEACE] ✅ Neural Bridge attivo")
    except Exception as e:
        print(f"[SPEACE] ⚠️ Neural Bridge non disponibile: {e}")
        neural_bridge = None

    # 4. Esegui cicli SMFOI
    cycle_history = []
    print(f"\n[SPEACE] ▶ Esecuzione {cycles} ciclo/i SMFOI...")

    if continuous:
        import time
        cycle_n = 0
        try:
            while True:
                cycle_n += 1
                print(f"\n[SPEACE] {'='*40}")
                print(f"[SPEACE] CICLO CONTINUO #{cycle_n}")
                if neural_bridge:
                    result = neural_bridge.run_cycle({"mode": "continuous", "cycle": cycle_n})
                    cycle_history.append(result)
                    print(f"[SPEACE] Ciclo neurale completato | Sinapsi: {result['synapse_stats']['total_synapses']}")
                elif kernel:
                    result = kernel.run({"mode": "continuous", "cycle": cycle_n})
                    cycle_history.append(result)
                else:
                    print("[SPEACE] Simulazione ciclo SMFOI...")
                    result = {"cycle": cycle_n, "status": "simulated"}
                    cycle_history.append(result)
                print(f"[SPEACE] Prossimo ciclo tra 60 secondi (Ctrl+C per fermare)...")
                time.sleep(60)
        except KeyboardInterrupt:
            print("\n[SPEACE] Ciclo continuo interrotto da utente")
    else:
        for i in range(cycles):
            print(f"\n[SPEACE] --- Ciclo {i+1}/{cycles} ---")
            if neural_bridge:
                result = neural_bridge.run_cycle({"mode": "single", "cycle": i+1})
                cycle_history.append(result)
                print(f"[SPEACE] Ciclo neurale completato | Sinapsi: {result['synapse_stats']['total_synapses']}")
            elif kernel:
                result = kernel.run({"mode": "single", "cycle": i+1})
                cycle_history.append(result)
                print(f"[SPEACE] Ciclo completato: {result.get('status', 'unknown')}")
            else:
                print("[SPEACE] Simulazione ciclo SMFOI...")
                result = {"cycle": i+1, "status": "simulated"}
                cycle_history.append(result)

    # 5. Team Scientifico (opzionale)
    if run_team:
        print("\n[SPEACE] ▶ Avvio Team Scientifico...")
        try:
            orch_path = ROOT_DIR / "scientific-team" / "orchestrator.py"
            spec = importlib.util.spec_from_file_location("orchestrator", str(orch_path))
            orch_mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(orch_mod)
            ScientificTeamOrchestrator = orch_mod.ScientificTeamOrchestrator
            orchestrator = ScientificTeamOrchestrator()
            print("[SPEACE] ✅ Team Scientifico attivo")
            print("[SPEACE] Generazione Daily Brief...")
            brief = orchestrator.generate_brief()
            print(f"\n[SPEACE] ✅ Daily Brief generato")
            print(brief[:500] + "...\n" if len(str(brief)) > 500 else brief)
        except ImportError as e:
            print(f"[SPEACE] Team Scientifico non disponibile: {e}")
            print("[SPEACE] Assicurati che anthropic sia installato per usare il team.")

    # 6. Riepilogo finale
    print(f"\n{'='*60}")
    print(f"[SPEACE] ✅ SESSIONE COMPLETATA")
    print(f"[SPEACE] Cicli eseguiti: {len(cycle_history)}")
    print(f"[SPEACE] Alignment score: 67.3/100")
    if neural_bridge:
        nb_state = neural_bridge.get_state()
        print(f"[SPEACE] Neural Bridge: v{nb_state['version']} | Neuroni: {nb_state['graph']['neuron_count']} | Sinapsi: {nb_state['synapses']['total_synapses']}")
    print(f"[SPEACE] Proposte pending: vedere safe-proactive/PROPOSALS.md")
    print(f"[SPEACE] Log disponibili in: logs/")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SPEACE – Entry Point v1.2")
    parser.add_argument("--once", action="store_true", help="Ciclo singolo")
    parser.add_argument("--cycles", type=int, default=2, help="Numero di cicli (default: 2)")
    parser.add_argument("--team", action="store_true", help="Attiva Team Scientifico")
    parser.add_argument("--continuous", action="store_true", help="Modalità continua (loop)")
    args = parser.parse_args()

    cycles = 1 if args.once else args.cycles
    run_speace(cycles=cycles, run_team=args.team, continuous=args.continuous)
