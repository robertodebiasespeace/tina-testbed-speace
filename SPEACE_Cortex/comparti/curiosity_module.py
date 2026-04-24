"""
Curiosity Module - Exploration & Novel Mutation Generation
Composto per esplorazione e generazione di novita.
Versione: 1.0
Data: 23 Aprile 2026
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import random
import logging

logger = logging.getLogger("CuriosityModule")


class CuriosityModule:
    """
    Curiosity Module - Exploration e Novel Mutation.

    Responsabilita:
    - Driven di esplorazione per informazione
    - Generazione di novita/mutazioni
    - Balancing exploration vs exploitation
    - Novelty detection
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.name = "curiosity_module"
        self.version = "1.1"
        self.config = config or {}
        self.bridge = None

        # Curiosity parameters
        self.exploration_rate = self.config.get("exploration_rate", 0.15)
        self.novelty_threshold = self.config.get("novelty_threshold", 0.7)

        # Tracked novelty
        self.known_concepts: set = set()
        self.novel_findings: List[Dict] = []
        self.mutations_proposed: List[Dict] = []
        self.max_mutations = self.config.get("max_mutations", 50)

        # Stats
        self.exploration_count = 0
        self.novelty_count = 0
        self.last_exploration = datetime.now()

    def set_bridge(self, bridge):
        """Imposta il riferimento al Neural Bridge"""
        self.bridge = bridge

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processo principale Curiosity Module.

        Args:
            context: Contesto con operation, input_data

        Returns:
            Dict con exploration_results
        """
        self.last_exploration = datetime.now()

        try:
            operation = context.get("operation", "explore")

            if operation == "explore":
                result = self._explore(context)
            elif operation == "generate_mutation":
                result = self._generate_mutation(context)
            elif operation == "assess_novelty":
                result = self._assess_novelty(context)
            elif operation == "balance_exploration":
                result = self._get_exploration_tradeoff(context)
            else:
                result = {"status": "unknown_operation"}

            return {
                "status": "success",
                "result": result,
                "comparto": self.name,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"CuriosityModule error: {e}")
            return {"status": "error", "error": str(e), "comparto": self.name}

    def _explore(self, context: Dict) -> Dict[str, Any]:
        """Esegue esplorazione"""
        domain = context.get("domain", "general")
        depth = context.get("depth", 3)

        self.exploration_count += 1

        # Simula scoperta
        findings = []
        for i in range(depth):
            novelty_score = random.uniform(0.5, 0.95)
            if novelty_score > self.novelty_threshold:
                finding = {
                    "finding": f"novel_pattern_{i}",
                    "domain": domain,
                    "novelty_score": novelty_score,
                    "timestamp": datetime.now().isoformat(),
                }
                findings.append(finding)
                self.novel_findings.append(finding)
                self.novelty_count += 1

        return {
            "domain": domain,
            "exploration_depth": depth,
            "findings": findings,
            "novel_findings_count": len(findings),
            "total_novel": len(self.novel_findings),
            "exploration_rate": self.exploration_rate,
        }

    def _generate_mutation(self, context: Dict) -> Dict[str, Any]:
        """Genera proposta di mutazione"""
        mutation_type = context.get("type", "random")
        target = context.get("target", "epigenome")

        # Template mutazioni
        mutation_templates = [
            {
                "type": "increase_exploration",
                "change": "+0.05 exploration_rate",
                "rationale": "Aumentare esplorazione per nuovi pattern",
                "expected_impact": "positive",
            },
            {
                "type": "yield_adjustment",
                "change": "yield_priority +/- 1",
                "rationale": "Ottimizzare priorita risorse",
                "expected_impact": "neutral",
            },
            {
                "type": "novel_mutation",
                "change": "add_new_behavior",
                "rationale": "Introduce new capability",
                "expected_impact": "unknown",
            },
        ]

        mutation = random.choice(mutation_templates)
        mutation.update({
            "id": f"mut_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "target": target,
            "timestamp": datetime.now().isoformat(),
        })

        self.mutations_proposed.append(mutation)

        if len(self.mutations_proposed) > self.max_mutations:
            self.mutations_proposed = self.mutations_proposed[-self.max_mutations:]

        return mutation

    def _assess_novelty(self, context: Dict) -> Dict[str, Any]:
        """Valuta novita di un input"""
        concept = context.get("concept", "")

        if concept in self.known_concepts:
            novelty = 0.2
            is_novel = False
        else:
            novelty = random.uniform(0.6, 0.95)
            is_novel = novelty > self.novelty_threshold
            if is_novel:
                self.known_concepts.add(concept)

        return {
            "concept": concept,
            "novelty_score": novelty,
            "is_novel": is_novel,
            "threshold": self.novelty_threshold,
            "known_count": len(self.known_concepts),
        }

    def _get_exploration_tradeoff(self, context: Dict) -> Dict[str, Any]:
        """Calcola tradeoff exploration vs exploitation"""
        current_exploration = self.exploration_rate
        fitness = context.get("fitness", 0.7)

        # Se fitness alto -> piu exploitation
        # Se fitness basso -> piu exploration
        if fitness > 0.75:
            recommended_exploration = max(0.05, current_exploration - 0.05)
            rationale = "High fitness - focus on exploitation"
        elif fitness < 0.5:
            recommended_exploration = min(0.3, current_exploration + 0.1)
            rationale = "Low fitness - need more exploration"
        else:
            recommended_exploration = current_exploration
            rationale = "Balanced - maintain current rate"

        return {
            "current_exploration": current_exploration,
            "recommended_exploration": recommended_exploration,
            "fitness_context": fitness,
            "rationale": rationale,
        }

    def add_known_concept(self, concept: str):
        """Aggiunge concetto gia conosciuto"""
        self.known_concepts.add(concept)

    def get_proposed_mutations(self, count: int = 10) -> List[Dict]:
        """API per ottenere mutazioni proposte"""
        return self.mutations_proposed[-count:]

    def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "exploration_rate": self.exploration_rate,
            "exploration_count": self.exploration_count,
            "novelty_count": self.novelty_count,
            "known_concepts": len(self.known_concepts),
            "mutations_proposed": len(self.mutations_proposed),
            "last_exploration": self.last_exploration.isoformat(),
        }
