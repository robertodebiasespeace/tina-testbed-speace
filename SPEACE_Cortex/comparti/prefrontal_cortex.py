"""
Prefrontal Cortex - Planning, Decision Making & Goal Management
Composto anteriore del cervello SPEACE per pianificazione e decisioni.
Versione: 1.0
Data: 23 Aprile 2026
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger("PrefrontalCortex")


class PrefrontalCortex:
    """
    Comparto Prefrontale - Planning, Decision Making e Goal Management.
    Interfaccia principale tra SMFOI-KERNEL e il resto del cervello.

    Responsabilita:
    - Generazione opzioni decisionali
    - Valutazione con Fitness + C-index
    - Pianificazione multi-step
    - Gestione obiettivi
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.name = "prefrontal_cortex"
        self.version = "1.0"
        self.config = config or {}
        self.bridge = None
        self.active_goals: List[Dict] = []
        self.decision_history: List[Dict] = []
        self.planning_depth = self.config.get("planning_depth", 5)
        self.max_options = self.config.get("max_options", 5)
        self.last_activation = datetime.now()
        self.activation_count = 0

    def set_bridge(self, bridge):
        """Imposta il riferimento al Neural Bridge"""
        self.bridge = bridge

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processo principale del comparto prefrontale.
        Data l'interfaccia sincrona per compatibilita con Neural Bridge.

        Args:
            context: Contesto con query, world_state, memory, ecc.

        Returns:
            Dict con decisione, confidence, fitness_delta
        """
        self.last_activation = datetime.now()
        self.activation_count += 1

        try:
            # Arricchisci contesto
            enriched = self._enrich_context(context)

            # Genera opzioni
            options = self._generate_decision_options(enriched)

            # Valuta opzioni
            evaluated = self._evaluate_options(options, enriched)

            # Seleziona migliore
            decision = self._select_best_decision(evaluated)

            # Log decisione
            self._log_decision(decision, enriched)

            return {
                "status": "success",
                "decision": decision,
                "confidence": decision.get("total_score", 0.5),
                "options_count": len(options),
                "comparto": self.name,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"PrefrontalCortex error: {e}")
            return {
                "status": "error",
                "error": str(e),
                "comparto": self.name,
            }

    def _enrich_context(self, context: Dict) -> Dict:
        """Arricchisce il contesto con dati dai altri comparti"""
        enriched = dict(context)
        enriched["_meta"] = {
            "planning_depth": self.planning_depth,
            "comparto": self.name,
            "activation": self.activation_count,
        }
        return enriched

    def _generate_decision_options(self, context: Dict) -> List[Dict[str, Any]]:
        """Genera multiple linee d'azione possibili"""
        options = []

        # Opzione 1: Esegui SMFOI step
        options.append({
            "action": "execute_smfoi_cycle",
            "priority": 0.9,
            "risk": 0.2,
            "description": "Esegui ciclo SMFOI completo",
        })

        # Opzione 2: Usa memoria Hermes (long-term memory)
        options.append({
            "action": "use_hermes_memory",
            "priority": 0.75,
            "risk": 0.1,
            "description": "Richiama memoria persistente e contesto da Hermes Agent",
        })

        # Opzione 3: Delega ad AGPT (task complessi)
        options.append({
            "action": "delegate_to_agpt",
            "priority": 0.7,
            "risk": 0.3,
            "description": "Delega task complesso a AutoGPT Forge per tool use",
        })

        # Opzione 3.5: Self-Dialogue (metacognizione)
        options.append({
            "action": "invoke_self_dialogue",
            "priority": 0.68,
            "risk": 0.05,
            "description": "Attiva Meta-Neurone Dialogico per riflessione e self-critique",
        })

        # Opzione 4: Esplora nuova mutazione
        options.append({
            "action": "explore_mutation",
            "priority": 0.65,
            "risk": 0.4,
            "description": "Genera e valuta nuova mutazione genetica",
        })

        # Opzione 5: Reflexione default mode
        options.append({
            "action": "invoke_default_mode",
            "priority": 0.6,
            "risk": 0.1,
            "description": "Attiva reflection e self-improvement",
        })

        # Opzione 6: Query memoria
        options.append({
            "action": "query_memory",
            "priority": 0.55,
            "risk": 0.05,
            "description": "Interroga hippocampus per ricordi rilevanti",
        })

        # Opzione 7: Check sicurezza
        options.append({
            "action": "safety_check",
            "priority": 0.95,
            "risk": 0.0,
            "description": "Verifica vincoli di sicurezza prima azione",
        })

        return options[: self.max_options]

    def _evaluate_options(
        self, options: List[Dict], context: Dict
    ) -> List[Dict]:
        """Valuta opzioni con fitness e awareness"""
        fitness = context.get("fitness", 0.7)
        c_index = context.get("c_index", 0.65)

        for opt in options:
            risk = opt.get("risk", 0.5)
            priority = opt.get("priority", 0.5)

            # Score: priorita alta + rischio basso = score alto
            opt["fitness_score"] = fitness * (1 - risk * 0.5)
            opt["consciousness_score"] = c_index * priority
            opt["total_score"] = (
                0.55 * opt["fitness_score"] + 0.45 * opt["consciousness_score"]
            )

        return sorted(options, key=lambda x: x.get("total_score", 0), reverse=True)

    def _select_best_decision(self, evaluated: List[Dict]) -> Dict:
        """Seleziona la decisione migliore"""
        if not evaluated:
            return {"action": "noop", "total_score": 0.3, "description": "Nessuna opzione"}
        return evaluated[0]

    def _log_decision(self, decision: Dict, context: Dict):
        """Registra la decisione nello storico"""
        self.decision_history.append({
            "timestamp": datetime.now().isoformat(),
            "action": decision.get("action"),
            "score": decision.get("total_score"),
            "description": decision.get("description", ""),
        })
        # Mantieni solo ultimi 100
        if len(self.decision_history) > 100:
            self.decision_history = self.decision_history[-100:]

    # === Goal Management ===

    def add_goal(self, goal: Dict[str, Any]) -> None:
        """Aggiunge un obiettivo alla lista attiva"""
        goal["added_at"] = datetime.now().isoformat()
        goal["status"] = "active"
        self.active_goals.append(goal)

    def get_active_goals(self) -> List[Dict]:
        """Ritorna gli obiettivi attivi"""
        return [g for g in self.active_goals if g.get("status") == "active"]

    def complete_goal(self, goal_id: str) -> bool:
        """Segna un obiettivo come completato"""
        for g in self.active_goals:
            if g.get("id") == goal_id:
                g["status"] = "completed"
                g["completed_at"] = datetime.now().isoformat()
                return True
        return False

    # === Status ===

    def get_status(self) -> Dict[str, Any]:
        """Ritorna lo stato del comparto"""
        return {
            "name": self.name,
            "version": self.version,
            "active_goals": len(self.get_active_goals()),
            "decisions_count": len(self.decision_history),
            "last_activation": self.last_activation.isoformat(),
            "activation_count": self.activation_count,
        }
