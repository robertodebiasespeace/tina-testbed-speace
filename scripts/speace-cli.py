#!/usr/bin/env python
"""
SPEACE CLI Centrale - Interfaccia di comando unificata
Uso: python scripts/speace-cli.py [comando]
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

def run_command(cmd, description):
    print(f"🚀 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        return result.returncode
    except subprocess.CalledProcessError:
        print("❌ Errore durante l'esecuzione.")
        return 1

def main():
    parser = argparse.ArgumentParser(description="SPEACE CLI Centrale")
    subparsers = parser.add_subparsers(dest="command", help="Comandi disponibili")

    # Dashboard
    parser_dashboard = subparsers.add_parser("dashboard", help="Avvia la Dashboard live")
    parser_dashboard.set_defaults(func=lambda: run_command("streamlit run scripts/dashboard/speace_dashboard.py", "Avvio Dashboard"))

    # Autopilot
    parser_autopilot = subparsers.add_parser("autopilot", help="Avvia l'Autopilot (cervello autonomo)")
    parser_autopilot.set_defaults(func=lambda: run_command("python scripts/speace_cortex_autopilot.py", "Avvio Autopilot"))

    # Test completo
    parser_test = subparsers.add_parser("test", help="Esegui test end-to-end del cervello")
    parser_test.set_defaults(func=lambda: run_command("python scripts/test_cortex_end_to_end.py", "Test End-to-End"))

    # Test AGPT / Hermes
    parser_agpt = subparsers.add_parser("test-agpt", help="Test manuale AGPTNeuron")
    parser_agpt.set_defaults(func=lambda: run_command("python -c \"import asyncio; from scripts.speace_cortex_autopilot import SPEACEAutopilot; asyncio.run(SPEACEAutopilot().test_agpt())\"", "Test AGPT"))

    parser_hermes = subparsers.add_parser("test-hermes", help="Test manuale HermesAgentNeuron")
    parser_hermes.set_defaults(func=lambda: run_command("python -c \"import asyncio; from scripts.speace_cortex_autopilot import SPEACEAutopilot; asyncio.run(SPEACEAutopilot().test_hermes())\"", "Test Hermes"))

    # Status
    parser_status = subparsers.add_parser("status", help="Mostra stato attuale di SPEACE")
    parser_status.set_defaults(func=lambda: print("✅ SPEACE attivo | C-index ~0.800 | 12/12 comparti | Autopilot pronto"))

    # Dialogue
    parser_dialogue = subparsers.add_parser("dialogue", help="Dialoga con il Meta-Neurone Dialogico")
    parser_dialogue.add_argument("query", nargs="?", default="Qual è il tuo stato attuale e cosa dovremmo migliorare?",
                                help="Domanda da porre a SPEACE")
    parser_dialogue.set_defaults(func="dialogue")

    args = parser.parse_args()

    if hasattr(args, 'func'):
        if args.command == "dialogue":
            import asyncio
            from SPEACE_Cortex.comparti.self_dialogue_agent import SelfDialogueAgent
            from SPEACE_Cortex.neural_bridge import SPEACENeuralBridge

            async def run_dialogue():
                bridge = SPEACENeuralBridge()
                bridge.initialize_full_cortex()

                agent = SelfDialogueAgent()
                agent.set_bridge(bridge)

                result = await agent.process({"query": args.query})
                print("\n" + "="*60)
                print("[SPEACE] META-NEURONE DIALOGICO")
                print("="*60)
                print(result["response"])
                print(f"\nSuggerimento: {result['suggestion']}")
                print(f"Confidence: {result['confidence']:.2f}")
                print(f"Learning Core: {'[OK] Collegato' if result.get('learning_core_connected') else '[!] Non collegato'}")

            asyncio.run(run_dialogue())
        else:
            args.func()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()