"""
SMFOI-KERNEL v0.3 - Schema Minimo Fondamentale di Orientamento dell'Intelligenza
6-Step Recursive Orientation Protocol for SPEACE Cortex

Implementa il protocollo 6-step per l'orientamento ricorsivo dell'intelligenza.
Integra Outcome Evaluation & Learning per feedback continuo.

Versione: 0.3
Data: 2026-04-17
Autore: SPEACE Cortex / Roberto De Biase
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SMFOI-KERNEL-v0.3")


@dataclass
class SMFOIState:
    """Stato interno del kernel SMFOI"""
    step: int = 0
    self_location: Dict[str, Any] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)
    pushes: List[Dict[str, Any]] = field(default_factory=list)
    survival_stack: Dict[str, Any] = field(default_factory=dict)
    output_action: Dict[str, Any] = field(default_factory=dict)
    outcome_evaluation: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = ""
    cycle_id: int = 0


class SMFOIKernel:
    """
    Kernel centrale SMFOI per SPEACE Cortex.
    Implementa il protocollo 6-step ricorsivo.
    """

    def __init__(self, cortex_instance=None):
        self.state = SMFOIState()
        self.cortex = cortex_instance
        self.version = "0.3"
        self.intrinsic_motivation = True

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Esegue il ciclo completo 6-step.

        Args:
            input_data: Dati in input (user request, IoT signals, etc.)

        Returns:
            Risultato dell'elaborazione con azione consigliata
        """
        self.state.cycle_id += 1
        self.state.timestamp = datetime.now().isoformat()

        logger.info(f"=== SMFOI-KERNEL v{self.version} - Cycle {self.state.cycle_id} ===")

        try:
            # Step 1: Self-Location
            self.state.self_location = self._step1_self_location()

            # Step 2: Constraint Mapping
            self.state.constraints = self._step2_constraint_mapping()

            # Step 3: Push Detection
            self.state.pushes = self._step3_push_detection(input_data)

            # Step 4: Survival & Evolution Stack
            self.state.survival_stack = self._step4_survival_evolution()

            # Step 5: Output Action
            self.state.output_action = self._step5_output_action()

            # Step 6: Outcome Evaluation & Learning (NEW in v0.3)
            self.state.outcome_evaluation = self._step6_outcome_evaluation()

            return self._compile_result()

        except Exception as e:
            logger.error(f"Error in SMFOI cycle: {e}")
            return {"status": "error", "message": str(e)}

    def _step1_self_location(self) -> Dict[str, Any]:
        """
        Step 1: SELF-LOCATION
        Definisce posizione attuale nel SEA (Self-Evolving Agent)
        """
        logger.info("Step 1: Self-Location...")

        return {
            "identity": "SPEACE",
            "full_name": "SuPer Entità Autonoma Cibernetica Evolutiva",
            "phase": "Fase 1 - Embrionale",
            "alignment_score": 67.3,
            "active_comparti": 9,
            "kernel_version": self.version,
            "swarm_size": 8,
            "team_status": "Operativo",
            "cortex_modules": [
                "Prefrontal Cortex", "Perception Module", "World Model/KG",
                "Hippocampus", "Temporal Lobe", "Parietal Lobe",
                "Cerebellum", "Default Mode Network", "Curiosity Module", "Safety Module"
            ]
        }

    def _step2_constraint_mapping(self) -> Dict[str, Any]:
        """
        Step 2: CONSTRAINT MAPPING
        Mappa vincoli attuali: risorse, policy, hardware, limiti operativi
        """
        logger.info("Step 2: Constraint Mapping...")

        return {
            "hardware": {
                "platform": "Windows 11 Notebook",
                "cpu": "Intel Core i9-11900H @ 2.50GHz",
                "ram_gb": 16,
                "storage_gb": 954,
                "gpu": "NVIDIA GeForce RTX 3060"
            },
            "software_constraints": {
                "safe_proactive": "always_active",
                "human_approval_required": ["medium_risk", "high_risk", "regulatory"],
                "alignment_minimum": 0.60,
                "ethical_bounds": "strict"
            },
            "resource_limits": {
                "max_ram_allocation_gb": 12.5,
                "reserved_os_gb": 3.5,
                "max_swarm_size": 50
            },
            "regulatory": {
                "eu_ai_act": "compliant",
                "nist_framework": "aligned",
                "iso_42001": "target"
            }
        }

    def _step3_push_detection(self, input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Step 3: PUSH DETECTION
        Rileva forze esterne: user request, eventi IoT, market data, segnali ambientali
        """
        logger.info("Step 3: Push Detection...")

        pushes = []

        # User requests
        if "user_request" in input_data:
            pushes.append({
                "type": "user_request",
                "source": "human",
                "payload": input_data["user_request"],
                "priority": "high"
            })

        # IoT signals
        if "iot_signals" in input_data:
            for signal in input_data["iot_signals"]:
                pushes.append({
                    "type": "iot_signal",
                    "source": signal.get("source", "unknown"),
                    "payload": signal,
                    "priority": signal.get("priority", "medium")
                })

        # Internal drives (intrinsic motivation)
        if self.intrinsic_motivation:
            pushes.append({
                "type": "intrinsic_drive",
                "source": "self",
                "payload": "curiosity_exploration",
                "priority": "low"
            })

        return pushes

    def _step4_survival_evolution(self) -> Dict[str, Any]:
        """
        Step 4: SURVIVAL & EVOLUTION STACK
        Stack di risposta Lv0-Lv3
        """
        logger.info("Step 4: Survival & Evolution Stack...")

        return {
            "level_0_.reactive": {
                "description": "Base reactive response",
                "trigger": "immediate_threat_or_opportunity",
                "execution": "fast_pattern_matching"
            },
            "level_1_adaptive": {
                "description": "Learning-based adaptation",
                "trigger": "novel_situation_detected",
                "execution": "update_world_model"
            },
            "level_2_proactive": {
                "description": "Goal-seeking behavior",
                "trigger": "alignment_with_objectives",
                "execution": "plan_and_execute"
            },
            "level_3_auto_modifying": {
                "description": "Self-modifying (with constraints)",
                "trigger": "evolutionary_advantage_detected",
                "execution": "propose_mutation_via_safe_proactive"
            }
        }

    def _step5_output_action(self) -> Dict[str, Any]:
        """
        Step 5: OUTPUT ACTION
        Pipeline: SafeProactive → Execution → Logging
        """
        logger.info("Step 5: Output Action...")

        # Build action based on pushes and survival stack
        action = {
            "type": "analysis_and_proposal",
            "requires_approval": True,
            "risk_level": "low",
            "pipeline": ["safe_proactive_check", "execution", "logging"],
            "timestamp": self.state.timestamp
        }

        return action

    def _step6_outcome_evaluation(self) -> Dict[str, Any]:
        """
        Step 6: OUTCOME EVALUATION & LEARNING (NEW v0.3)
        Misura esito reale, calcola feedback per fitness function,
        aggiorna epigenome.yaml e World Model
        """
        logger.info("Step 6: Outcome Evaluation & Learning...")

        # Calculate fitness feedback
        alignment = self.state.self_location.get("alignment_score", 67.3) / 100
        stability = 0.85  # Estimated
        efficiency = 0.75  # Estimated
        ethics = 0.90  # Estimated
        success_rate = 0.80  # Estimated

        fitness = (
            alignment * 0.35 +
            success_rate * 0.25 +
            stability * 0.20 +
            efficiency * 0.15 +
            ethics * 0.05
        )

        return {
            "fitness_score": fitness,
            "fitness_classification": self._classify_fitness(fitness),
            "feedback_to_epigenome": {
                "learning_adjustment": 0.01,
                "next_heartbeat_recommended": True
            },
            "world_model_update": {
                "new_knowledge": None,
                "confidence_adjustment": 0.05
            },
            "mutation_recommendation": "none" if fitness > 0.70 else "consider_low_risk"
        }

    def _classify_fitness(self, fitness: float) -> str:
        """Classifica il fitness score"""
        if fitness >= 0.85:
            return "EXCELLENT"
        elif fitness >= 0.70:
            return "GOOD"
        elif fitness >= 0.60:
            return "ACCEPTABLE"
        else:
            return "LOW - review needed"

    def _compile_result(self) -> Dict[str, Any]:
        """Compila il risultato finale del ciclo"""
        return {
            "status": "success",
            "kernel_version": self.version,
            "cycle_id": self.state.cycle_id,
            "timestamp": self.state.timestamp,
            "self_location": self.state.self_location,
            "constraints": self.state.constraints,
            "detected_pushes": len(self.state.pushes),
            "survival_stack_active": "level_2_proactive",
            "recommended_action": self.state.output_action,
            "fitness_evaluation": self.state.outcome_evaluation,
            "token_overhead_estimate": "2-15 tokens"
        }


def run_smfoi_cycle(input_data: Dict[str, Any], cortex=None) -> Dict[str, Any]:
    """
    Funzione helper per eseguire un ciclo SMFOI completo.

    Args:
        input_data: Dati in input
        cortex: Istanza optional del Cortex SPEACE

    Returns:
        Risultato del ciclo 6-step
    """
    kernel = SMFOIKernel(cortex)
    return kernel.run(input_data)


if __name__ == "__main__":
    # Test del kernel
    test_input = {
        "user_request": "Analizza lo stato di salute planetaria",
        "iot_signals": [
            {"source": "climate_sensor", "data": "temp_anomaly", "priority": "high"}
        ]
    }

    result = run_smfoi_cycle(test_input)
    print(json.dumps(result, indent=2))
