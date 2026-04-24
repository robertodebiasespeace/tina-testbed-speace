"""
SPEACE Cortex Orchestrator - Coordinatore Centrale dei 9 Comparti
Versione: 1.0
Data: 23 Aprile 2026
"""

from typing import Dict, Any
from datetime import datetime
import asyncio
import logging

logger = logging.getLogger("CortexOrchestrator")


class CortexOrchestrator:
    """
    Orchestratore centrale del cervello SPEACE.
    Coordina i 9 comparti, integra SMFOI, DigitalDNA e Adaptive Consciousness.
    """

    def __init__(self, neural_bridge):
        self.bridge = neural_bridge
        self.compartments = neural_bridge.compartments
        self.smfoi = None  # Inizializzato lazily
        self.last_cycle = datetime.now()
        self.cycle_count = 0

    async def run_cycle(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Esegue un ciclo cognitivo completo end-to-end"""
        self.last_cycle = datetime.now()
        self.cycle_count += 1
        logger.info(f"[CortexOrchestrator] Ciclo #{self.cycle_count} - Inizio")

        results = {
            "cycle_id": self.cycle_count,
            "timestamp": self.last_cycle.isoformat(),
            "input": input_data,
            "compartments": {},
            "smfoi_outcome": None,
            "fitness_delta": 0.0,
            "c_index": 0.712,
            "status": "success"
        }

        try:
            # 1. Prefrontal Cortex decide la strategia (sincrono per ora)
            if "prefrontal" in self.compartments:
                comp = self.compartments["prefrontal"]
                try:
                    prefrontal_result = comp.process(input_data)
                    results["compartments"]["prefrontal"] = prefrontal_result
                except Exception as e:
                    logger.error(f"Prefrontal error: {e}")
                    results["compartments"]["prefrontal"] = {"status": "error", "error": str(e)}

            # 2. Safety check sempre
            if "safety" in self.compartments:
                comp = self.compartments["safety"]
                try:
                    safety_result = comp.process({
                        "operation": "assess_risk",
                        "action": "cortex_cycle"
                    })
                    results["compartments"]["safety"] = safety_result
                except Exception as e:
                    results["compartments"]["safety"] = {"status": "error", "error": str(e)}

            # 3. Esecuzione comparti rimanenti
            for name, comp in self.compartments.items():
                if name in ["prefrontal", "safety"]:
                    continue

                try:
                    compartment_result = comp.process(input_data)
                    results["compartments"][name] = compartment_result
                except Exception as e:
                    logger.error(f"Compartment {name} error: {e}")
                    results["compartments"][name] = {"status": "error", "error": str(e)}

            # 3.5 Delega neuroni esterni (Hermes, AGPT) basato su decisione Prefrontal
            prefrontal_decision = results.get("compartments", {}).get("prefrontal", {}).get("decision", {})
            action = str(prefrontal_decision.get("action", ""))

            if "use_hermes_memory" in action:
                hermes_comp = self.compartments.get("hermes") or (self.bridge.compartments.get("hermes") if hasattr(self.bridge, 'compartments') else None)
                if hermes_comp:
                    try:
                        hermes_result = hermes_comp.process({
                            "query": "Richiamo contesto precedente per ciclo cognitivo",
                            "mode": "recall",
                            "timestamp": datetime.now().isoformat()
                        })
                        results["compartments"]["hermes"] = hermes_result
                        logger.info("Hermes memory recall attivato")
                    except Exception as e:
                        logger.warning(f"Hermes error: {e}")

            if "delegate_to_agpt" in action:
                agpt_comp = self.compartments.get("agpt") or (self.bridge.compartments.get("agpt") if hasattr(self.bridge, 'compartments') else None)
                if agpt_comp:
                    try:
                        agpt_result = agpt_comp.process({
                            "task": prefrontal_decision.get("description", "Task delegato da Prefrontal"),
                            "context": input_data
                        })
                        results["compartments"]["agpt"] = agpt_result
                        logger.info("AGPT task delegation attivata")
                    except Exception as e:
                        logger.warning(f"AGPT error: {e}")

            # 4. SMFOI-KERNEL outcome
            results["smfoi_outcome"] = self._generate_smfoi_outcome(results)

            # 5. Calcola fitness delta
            results["fitness_delta"] = self._calculate_fitness_delta(results)

            # 6. C-index (placeholder)
            results["c_index"] = self._calculate_c_index(results)

            # === MUTAZIONI EPIGENETICHE AUTOMATICHE ===
            if hasattr(self.bridge, 'learning_core') and self.bridge.learning_core:
                try:
                    metrics = self.bridge.learning_core.get_metrics()
                    if metrics.get("avg_fitness", 0) > 0.75 and results["c_index"] > 0.78:
                        from DigitalDNA.mutation_rules import apply_epigenetic_mutation
                        mutation = apply_epigenetic_mutation("positive", {"c_index": results["c_index"]})
                        logger.info(f"🧬 Mutazione epigenetica positiva applicata: {mutation}")
                except Exception as e:
                    logger.debug(f"Mutazione epigenetica skip: {e}")

            logger.info(f"[CortexOrchestrator] Ciclo #{self.cycle_count} completato - "
                       f"C-index: {results['c_index']:.3f}, Fitness delta: {results['fitness_delta']:+.3f}")

        except Exception as e:
            logger.error(f"Cycle error: {e}")
            results["status"] = "error"
            results["error"] = str(e)

        return results

    def _generate_smfoi_outcome(self, results: Dict) -> Dict[str, Any]:
        """Genera outcome SMFOI basato sui risultati dei comparti"""
        # Usa il prefrontal decision se disponibile
        prefrontal = results.get("compartments", {}).get("prefrontal", {})
        if isinstance(prefrontal, dict) and "decision" in prefrontal:
            decision = prefrontal["decision"]
            return {
                "action": decision.get("action", "noop"),
                "confidence": decision.get("confidence", 0.5),
                "status": "completed"
            }

        # Default outcome
        return {
            "action": "process_cortex_cycle",
            "confidence": 0.7,
            "status": "completed"
        }

    def _calculate_fitness_delta(self, results: Dict) -> float:
        """Calcola delta fitness basato su performance"""
        c_index = results.get("c_index", 0.7)

        if c_index > 0.75:
            return 0.05
        elif c_index > 0.65:
            return 0.02
        else:
            return -0.03

    def _calculate_c_index(self, results: Dict) -> float:
        """Calcola C-index basato su stato comparti"""
        compartments = results.get("compartments", {})

        if not compartments:
            return 0.5

        # Conta comparti con successo
        success_count = sum(
            1 for r in compartments.values()
            if isinstance(r, dict) and r.get("status") == "success"
        )

        base_c_index = 0.65
        compartment_factor = success_count / max(len(compartments), 1) * 0.15

        return min(0.95, base_c_index + compartment_factor)

    async def run_full_cognitive_cycle(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Alias for run_cycle for compatibility"""
        return await self.run_cycle(input_data)
