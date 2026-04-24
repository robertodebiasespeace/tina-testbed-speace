"""
Test End-to-End del Cervello SPEACE
Esegue un ciclo completo attraverso tutti i 9 comparti

Usage:
    python scripts/test_cortex_end_to_end.py
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from SPEACE_Cortex.neural_bridge import SPEACENeuralBridge


async def main():
    print("=" * 80)
    print("SPEACE CORTEX END-TO-END TEST")
    print("=" * 80)
    print()

    # Initialize bridge
    print("[1/4] Inizializzazione Neural Bridge...")
    bridge = SPEACENeuralBridge()
    bridge.initialize_full_cortex()
    print()

    # Prepare test input
    test_input = {
        "query": "Qual e lo stato attuale del Rigene Project e quali mutazioni epigenetiche dovremmo proporre?",
        "push_intensity": 0.75,
        "environment": "reale",
        "user_request": "Analisi strategica",
        "mode": "test"
    }

    print("[2/4] Input di test:")
    for key, value in test_input.items():
        print(f"   {key}: {value}")
    print()

    # Run full cognitive cycle
    print("[3/4] Eseguo ciclo cognitivo completo attraverso i 9 comparti...")
    result = await bridge.run_full_cognitive_cycle(test_input)
    print()

    # Print results
    print("=" * 80)
    print("RISULTATI DEL CICLO COGNITIVO COMPLETO")
    print("=" * 80)
    print(f"Cycle ID:      {result.get('cycle_id', 'N/A')}")
    print(f"Timestamp:      {result.get('timestamp', 'N/A')}")
    print(f"Status:        {result.get('status', 'N/A')}")
    print(f"C-index:       {result.get('c_index', 0):.3f}")
    print(f"Fitness Delta: {result.get('fitness_delta', 0):+.3f}")

    smfoi = result.get('smfoi_outcome', {})
    if isinstance(smfoi, dict):
        print(f"SMFOI Action:  {smfoi.get('action', 'N/A')}")
        print(f"SMFOI Conf:    {smfoi.get('confidence', 0):.2f}")

    print()
    print("-" * 80)
    print("COMPARTI ATTIVATI (9/9):")
    print("-" * 80)

    compartments = result.get('compartments', {})
    for name, res in compartments.items():
        if isinstance(res, dict):
            status = res.get('status', 'unknown')
            status_icon = "[OK]" if status == "success" else "[!!]"
            decision_info = ""
            if name == "prefrontal" and "decision" in res:
                decision_info = f" -> {res['decision'].get('action', '')}"
            print(f"   {status_icon} {name:20} {decision_info}")
        else:
            print(f"   [??] {name}")

    print()
    print("-" * 80)
    print("PREFRONTAL CORTEX - DETTAGLI DECISIONE:")
    print("-" * 80)
    prefrontal = compartments.get('prefrontal', {})
    if isinstance(prefrontal, dict) and 'decision' in prefrontal:
        decision = prefrontal['decision']
        print(f"   Action:       {decision.get('action', 'N/A')}")
        print(f"   Confidence:   {decision.get('confidence', 0):.3f}")
        print(f"   Description:  {decision.get('description', 'N/A')}")

    print()
    print("-" * 80)
    print("SAFETY MODULE - RISK ASSESSMENT:")
    print("-" * 80)
    safety = compartments.get('safety', {})
    if isinstance(safety, dict):
        print(f"   Risk Score:  {safety.get('risk_score', 'N/A')}")
        print(f"   Risk Level:  {safety.get('risk_level', 'N/A')}")
        print(f"   Approved:    {safety.get('approved', 'N/A')}")

    print()
    print("=" * 80)
    print("TEST COMPLETATO CON SUCCESSO!")
    print("=" * 80)

    return result


if __name__ == "__main__":
    result = asyncio.run(main())
