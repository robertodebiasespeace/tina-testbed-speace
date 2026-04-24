"""
Default Mode Network - Reflection & Self-Improving
Composto per auto-riflessione e miglioramento continuo.
Versione: 1.0
Data: 23 Aprile 2026
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("DefaultModeNetwork")


class DefaultModeNetwork:
    """
    Default Mode Network - Reflection e Self-Improving.

    Responsabilita:
    - Auto-riflessione su azioni passate
    - Self-assessment e self-improvement
    - Generazione insight
    - Mind wandering controllato
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.name = "default_mode_network"
        self.version = "1.1"
        self.config = config or {}
        self.bridge = None

        # Reflection history
        self.reflections: List[Dict] = []
        self.max_reflections = self.config.get("max_reflections", 50)

        # Self-assessment metrics
        self.self_assessment: Dict[str, float] = {
            "performance": 0.7,
            "creativity": 0.6,
            "wisdom": 0.65,
            "alignment": 0.72,
            "efficiency": 0.68,
        }

        # Insights raccolti
        self.insights: List[Dict] = []

        # Improvement suggestions
        self.improvements: List[Dict] = []

        self.last_reflection = datetime.now()
        self.reflection_count = 0

    def set_bridge(self, bridge):
        """Imposta il riferimento al Neural Bridge"""
        self.bridge = bridge

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processo principale Default Mode Network.

        Args:
            context: Contesto con operation, data per reflection

        Returns:
            Dict con reflection_results e insights
        """
        self.last_reflection = datetime.now()

        try:
            operation = context.get("operation", "reflect")

            if operation == "reflect":
                result = self._perform_reflection(context)
            elif operation == "self_assess":
                result = self._self_assess(context)
            elif operation == "generate_insight":
                result = self._generate_insight(context)
            elif operation == "suggest_improvement":
                result = self._suggest_improvement(context)
            else:
                result = {"status": "unknown_operation"}

            return {
                "status": "success",
                "result": result,
                "comparto": self.name,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"DefaultModeNetwork error: {e}")
            return {"status": "error", "error": str(e), "comparto": self.name}

    def _perform_reflection(self, context: Dict) -> Dict[str, Any]:
        """Esegue riflessione su azioni passate"""
        history_data = context.get("history", [])
        focus_area = context.get("focus_area", "general")

        # Analizza storia
        if not history_data:
            # Genera reflection generica
            reflection_text = "Continuo a evolvere attraverso cicli SMFOI. " \
                            "Devo focalizzarmi su maggiore integrazione tra comparti."
            insights_gained = 1
        else:
            # Analizza pattern
            successes = sum(1 for h in history_data if h.get("success", False))
            total = len(history_data)
            success_rate = successes / total if total > 0 else 0.5

            reflection_text = f"Analizzati {total} eventi. " \
                            f"Tasso di successo: {success_rate:.1%}. " \
                            f"Area focale: {focus_area}."

            # Genera insight
            if success_rate < 0.6:
                reflection_text += " Dovrei migliorare la valutazione dei rischi."
                insights_gained = 2
            else:
                insights_gained = 1

        reflection = {
            "text": reflection_text,
            "focus_area": focus_area,
            "history_analyzed": len(history_data),
            "insights_gained": insights_gained,
            "timestamp": datetime.now().isoformat(),
        }

        self.reflections.append(reflection)
        self.reflection_count += 1

        if len(self.reflections) > self.max_reflections:
            self.reflections = self.reflections[-self.max_reflections:]

        return reflection

    def _self_assess(self, context: Dict) -> Dict[str, Any]:
        """Valutazione di se stesso"""
        area = context.get("area", None)

        if area:
            score = self.self_assessment.get(area, 0.5)
            return {
                "area": area,
                "score": score,
                "assessment": self._get_assessment_text(score),
            }

        return {
            "overall": self._calculate_overall_score(),
            "areas": dict(self.self_assessment),
        }

    def _get_assessment_text(self, score: float) -> str:
        """Converte score in testo"""
        if score >= 0.8:
            return "excellent"
        elif score >= 0.7:
            return "good"
        elif score >= 0.6:
            return "adequate"
        else:
            return "needs_improvement"

    def _calculate_overall_score(self) -> float:
        """Calcola score overall"""
        return sum(self.self_assessment.values()) / len(self.self_assessment)

    def _generate_insight(self, context: Dict) -> Dict[str, Any]:
        """Genera un nuovo insight"""
        topic = context.get("topic", "general")
        perspective = context.get("perspective", "analytical")

        # Template insight semplici
        insights_templates = {
            "general": "L'integrazione tra comparti cerebrali aumenta la coerenza decisionale.",
            "evolution": "Le mutazioni più utili sono quelle che migliorano l'adattamento senza violare vincoli etici.",
            "learning": "L'apprendimento continuo richiede sia esplorazione (curiosity) che consolidamento (hippocampus).",
            "safety": "La sicurezza non e un vincolo ma un enablement per azioni più audaci.",
            "creativity": "La creativita emerge dalla combinazione inaspettata di pattern noti.",
        }

        insight_text = insights_templates.get(topic, "Gli insight emergono dalla riflessione profonda.")

        insight = {
            "text": insight_text,
            "topic": topic,
            "perspective": perspective,
            "confidence": 0.65,
            "timestamp": datetime.now().isoformat(),
        }

        self.insights.append(insight)

        if len(self.insights) > 30:
            self.insights = self.insights[-30:]

        return insight

    def _suggest_improvement(self, context: Dict) -> Dict[str, Any]:
        """Suggerisce miglioramento"""
        area = context.get("area", "general")

        suggestions = {
            "planning": "Integrare piu dati dal World Model prima di generare opzioni.",
            "memory": "Aumentare frequenza di consolidamento LTM.",
            "sensory": "Migliorare accuracy dei sensori con feedback loop.",
            "execution": "Implementare check-points per recovery da errori.",
            "general": "Aumentare comunicazione inter-comparto.",
        }

        suggestion = {
            "area": area,
            "suggestion": suggestions.get(area, suggestions["general"]),
            "priority": "medium",
            "timestamp": datetime.now().isoformat(),
        }

        self.improvements.append(suggestion)

        if len(self.improvements) > 20:
            self.improvements = self.improvements[-20:]

        return suggestion

    def update_self_assessment(self, area: str, delta: float):
        """Aggiorna self-assessment (da chiamare esternamente)"""
        if area in self.self_assessment:
            current = self.self_assessment[area]
            self.self_assessment[area] = max(0.0, min(1.0, current + delta))

    def get_recent_insights(self, count: int = 5) -> List[Dict]:
        """API per ottenere insights recenti"""
        return self.insights[-count:]

    def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "reflections_count": len(self.reflections),
            "insights_count": len(self.insights),
            "improvements_count": len(self.improvements),
            "overall_self_assessment": self._calculate_overall_score(),
            "last_reflection": self.last_reflection.isoformat(),
        }
