"""
World Model Knowledge - Knowledge Graph & World State Representation
Composto per il modello interno della realta e inferenza.
Versione: 1.0
Data: 23 Aprile 2026
"""

from typing import Dict, Any, List, Optional, Set, Tuple
from datetime import datetime
import logging

logger = logging.getLogger("WorldModelKnowledge")


class WorldModelKnowledge:
    """
    World Model / Knowledge Graph - Modello interno della realta.

    Responsabilita:
    - Rappresentazione della conoscenza come grafo
    - Inferenza causale e temporale
    - Simulazione scenari futuri
    - Query e reasoning sulla struttura del mondo
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.name = "world_model_knowledge"
        self.version = "1.0"
        self.config = config or {}
        self.bridge = None

        # Knowledge Graph base (triples: subject, predicate, object)
        self.kg_triples: List[Tuple[str, str, str]] = []
        self.entities: Set[str] = set()
        self.predicates: Set[str] = set()

        # World state
        self.world_state: Dict[str, Any] = {}
        self.state_history: List[Dict] = []

        # Inference cache
        self.inference_cache: Dict[str, Any] = {}
        self.last_update = datetime.now()
        self.update_count = 0

        # Inizializza KG base
        self._initialize_base_knowledge()

    def set_bridge(self, bridge):
        """Imposta il riferimento al Neural Bridge"""
        self.bridge = bridge

    def _initialize_base_knowledge(self):
        """Inizializza conoscenza base"""
        base_triples = [
            ("SPEACE", "is_a", "Cybernetic_Organism"),
            ("SPEACE", "has_component", "Neural_Engine"),
            ("SPEACE", "has_component", "SMFOI_Kernel"),
            ("SPEACE", "has_goal", "Super_Intelligence"),
            ("Neural_Engine", "implements", "Computational_Graph"),
            ("SMFOI_Kernel", "implements", "6Step_Protocol"),
            ("DigitalDNA", "governs", "SPEACE_Evolution"),
            ("SafeProactive", "provides", "Safety_Gates"),
            ("SPEACE", "aligned_with", "TINA_Framework"),
            ("SPEACE", "phase", "Embryonic_1"),
        ]
        for triple in base_triples:
            self._add_triple(triple)

    def _add_triple(self, triple: Tuple[str, str, str]):
        """Aggiunge un triple al KG"""
        s, p, o = triple
        self.kg_triples.append(triple)
        self.entities.add(s)
        self.entities.add(o)
        self.predicates.add(p)

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processo principale World Model.

        Args:
            context: Contesto con query, update, infer

        Returns:
            Dict con world_model_results
        """
        self.last_update = datetime.now()
        self.update_count += 1

        try:
            operation = context.get("operation", "query")

            if operation == "query":
                result = self._query_knowledge(context)
            elif operation == "update":
                result = self._update_world_state(context)
            elif operation == "infer":
                result = self._infer_new_knowledge(context)
            elif operation == "simulate":
                result = self._simulate_scenario(context)
            else:
                result = {"status": "unknown_operation"}

            return {
                "status": "success",
                "result": result,
                "kg_size": len(self.kg_triples),
                "entities": len(self.entities),
                "comparto": self.name,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"WorldModelKnowledge error: {e}")
            return {"status": "error", "error": str(e), "comparto": self.name}

    def _query_knowledge(self, context: Dict) -> Dict[str, Any]:
        """Interroga il knowledge graph"""
        query = context.get("query", "")
        query_type = context.get("query_type", "entity")

        if query_type == "entity":
            results = self._get_entity_knowledge(query)
        elif query_type == "relationship":
            results = self._get_relationships(query)
        elif query_type == "path":
            results = self._find_path(context.get("from", ""), context.get("to", ""))
        else:
            results = {"matches": []}

        return {
            "query": query,
            "query_type": query_type,
            "results": results,
            "found": len(results.get("matches", [])),
        }

    def _get_entity_knowledge(self, entity: str) -> Dict[str, Any]:
        """Ottieni tutta la conoscenza su un'entita"""
        matches = [
            {"subject": s, "predicate": p, "object": o}
            for s, p, o in self.kg_triples
            if s == entity or o == entity
        ]
        return {"matches": matches}

    def _get_relationships(self, predicate: str) -> Dict[str, Any]:
        """Ottieni tutte le triple con un predicato"""
        matches = [
            {"subject": s, "predicate": p, "object": o}
            for s, p, o in self.kg_triples
            if p == predicate
        ]
        return {"matches": matches}

    def _find_path(self, from_entity: str, to_entity: str) -> Dict[str, Any]:
        """Trova path tra due entita (BFS semplificato)"""
        # BFS semplificato - depth limit 3
        visited = {from_entity}
        queue = [(from_entity, [from_entity])]

        while queue:
            current, path = queue.pop(0)
            if current == to_entity:
                return {"path": path, "length": len(path) - 1}

            if len(path) > 3:
                continue

            for s, p, o in self.kg_triples:
                if s == current and o not in visited:
                    visited.add(o)
                    queue.append((o, path + [o]))
                if o == current and s not in visited:
                    visited.add(s)
                    queue.append((s, path + [s]))

        return {"path": [], "length": -1, "found": False}

    def _update_world_state(self, context: Dict) -> Dict[str, Any]:
        """Aggiorna lo stato del mondo"""
        updates = context.get("updates", {})
        old_state = dict(self.world_state)

        for key, value in updates.items():
            self.world_state[key] = value

        # Registra in history
        self.state_history.append({
            "timestamp": datetime.now().isoformat(),
            "changes": updates,
            "old_state": old_state,
        })

        # Mantieni solo ultimi 50
        if len(self.state_history) > 50:
            self.state_history = self.state_history[-50:]

        return {
            "updated": list(updates.keys()),
            "current_state": self.world_state,
        }

    def _infer_new_knowledge(self, context: Dict) -> Dict[str, Any]:
        """Inferisce nuova conoscenza (deduzione semplice)"""
        entity = context.get("entity", "")

        # Regole di inferenza semplici
        inferred = []

        # Se X has_component Y e Y implements Z -> X implements Z
        for s1, p1, o1 in self.kg_triples:
            if p1 == "has_component":
                for s2, p2, o2 in self.kg_triples:
                    if s2 == o1 and p2 == "implements":
                        new_triple = (s1, "indirectly_implements", o2)
                        if new_triple not in self.kg_triples:
                            self._add_triple(new_triple)
                            inferred.append(new_triple)

        return {
            "inferred": inferred,
            "count": len(inferred),
        }

    def _simulate_scenario(self, context: Dict) -> Dict[str, Any]:
        """Simula uno scenario futuro"""
        scenario = context.get("scenario", {})
        horizon = context.get("horizon", 3)

        # Simulazione molto semplificata
        simulation = {
            "scenario": scenario,
            "horizon": horizon,
            "predicted_outcome": "success",
            "confidence": 0.65,
            "steps": horizon,
        }

        return simulation

    def add_knowledge(self, subject: str, predicate: str, obj: str):
        """API publica per aggiungere conoscenza"""
        self._add_triple((subject, predicate, obj))

    def get_world_state(self) -> Dict[str, Any]:
        """Ritorna stato attuale del mondo"""
        return dict(self.world_state)

    def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "kg_triples": len(self.kg_triples),
            "entities": len(self.entities),
            "predicates": len(self.predicates),
            "last_update": self.last_update.isoformat(),
            "update_count": self.update_count,
        }
