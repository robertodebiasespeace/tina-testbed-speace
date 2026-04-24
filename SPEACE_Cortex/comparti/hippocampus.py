"""
Hippocampus - Memory & Long-term Storage
Composto per la memoria a lungo termine e consolidamento.
Versione: 1.0
Data: 23 Aprile 2026
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import logging

logger = logging.getLogger("Hippocampus")


class Hippocampus:
    """
    Hippocampus - Memoria e Long-term Storage.

    Responsabilita:
    - Encoding e consolidamento memoria episodica
    - Recall di memorie rilevanti
    - Consolidamento LTM (Long-Term Memory)
    - Pattern separation e completion
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.name = "hippocampus"
        self.version = "1.0"
        self.config = config or {}
        self.bridge = None

        # Memoria episodica: lista di eventi
        self.episodes: List[Dict[str, Any]] = []
        self.max_episodes = self.config.get("max_episodes", 1000)

        # Memoria semantica (facts)
        self.semantic_memory: Dict[str, Any] = {}

        # Short-term / working memory
        self.working_memory: Dict[str, Any] = {}
        self.working_memory_size = self.config.get("working_memory_size", 7)

        # Index per recall rapido
        self.entity_index: Dict[str, List[int]] = {}  # entity -> episode indices
        self.temporal_index: List[str] = []  # timestamps

        self.last_access = datetime.now()
        self.recall_count = 0
        self.encoding_count = 0

    def set_bridge(self, bridge):
        """Imposta il riferimento al Neural Bridge"""
        self.bridge = bridge

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processo principale Hippocampus.

        Args:
            context: Contesto con operation (encode, recall, consolidate)

        Returns:
            Dict con memory_results
        """
        self.last_access = datetime.now()

        try:
            operation = context.get("operation", "recall")

            if operation == "encode":
                result = self._encode_episode(context)
            elif operation == "recall":
                result = self._recall_memories(context)
            elif operation == "consolidate":
                result = self._consolidate_ltm(context)
            elif operation == "working_memory":
                result = self._update_working_memory(context)
            else:
                result = {"status": "unknown_operation"}

            return {
                "status": "success",
                "result": result,
                "episodes_stored": len(self.episodes),
                "comparto": self.name,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Hippocampus error: {e}")
            return {"status": "error", "error": str(e), "comparto": self.name}

    def _encode_episode(self, context: Dict) -> Dict[str, Any]:
        """Codifica un nuovo episodio"""
        episode = {
            "id": f"ep_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self.encoding_count}",
            "timestamp": datetime.now().isoformat(),
            "content": context.get("content", ""),
            "entities": context.get("entities", []),
            "emotion": context.get("emotion", "neutral"),
            "importance": context.get("importance", 0.5),
            "context": context.get("episode_context", {}),
        }

        self.episodes.append(episode)
        self.encoding_count += 1

        # Aggiorna indices
        for entity in episode.get("entities", []):
            if entity not in self.entity_index:
                self.entity_index[entity] = []
            self.entity_index[entity].append(len(self.episodes) - 1)

        self.temporal_index.append(episode["timestamp"])

        # Enforce max size
        if len(self.episodes) > self.max_episodes:
            removed = self.episodes.pop(0)
            # Cleanup index
            for entity, indices in self.entity_index.items():
                if 0 in indices:
                    indices.remove(0)
                self.entity_index[entity] = [i - 1 for i in indices if i > 0]

        return {
            "encoded": True,
            "episode_id": episode["id"],
            "total_episodes": len(self.episodes),
        }

    def _recall_memories(self, context: Dict) -> Dict[str, Any]:
        """Richiama memorie rilevanti"""
        query = context.get("query", "")
        query_type = context.get("recall_type", "similarity")
        max_results = context.get("max_results", 5)

        self.recall_count += 1
        results = []

        if query_type == "entity":
            # Recall by entity
            indices = self.entity_index.get(query, [])
            results = [self.episodes[i] for i in indices[-max_results:]]
        elif query_type == "temporal":
            # Recall by time window
            time_from = context.get("time_from", "")
            time_to = context.get("time_to", datetime.now().isoformat())
            results = [
                ep for ep in self.episodes
                if time_from <= ep["timestamp"] <= time_to
            ][-max_results:]
        elif query_type == "importance":
            # Recall high importance
            threshold = context.get("threshold", 0.7)
            results = [
                ep for ep in self.episodes
                if ep.get("importance", 0) >= threshold
            ][-max_results:]
        else:
            # Recent recall
            results = self.episodes[-max_results:]

        return {
            "query": query,
            "results": results,
            "count": len(results),
            "recall_type": query_type,
        }

    def _consolidate_ltm(self, context: Dict) -> Dict[str, Any]:
        """Consolida memorie in LTM ( Long-Term Memory)"""
        # Simulazione consolidamento
        episodes_to_consolidate = context.get("episodes", self.episodes[-10:])

        consolidated = []
        for ep in episodes_to_consolidate:
            # Estrai fatti per memoria semantica
            if ep.get("entities"):
                key = f"fact_{ep['entities'][0]}"
                self.semantic_memory[key] = {
                    "content": ep.get("content"),
                    "timestamp": ep.get("timestamp"),
                    "consolidated_from": ep["id"],
                }
                consolidated.append(key)

        return {
            "consolidated": consolidated,
            "semantic_memory_size": len(self.semantic_memory),
            "episodes_processed": len(consolidated),
        }

    def _update_working_memory(self, context: Dict) -> Dict[str, Any]:
        """Aggiorna working memory"""
        operation = context.get("wm_op", "add")

        if operation == "add":
            key = context.get("key")
            value = context.get("value")
            if key and len(self.working_memory) < self.working_memory_size:
                self.working_memory[key] = value
            elif key:
                # Replace oldest
                oldest = list(self.working_memory.keys())[0]
                del self.working_memory[oldest]
                self.working_memory[key] = value

        elif operation == "clear":
            self.working_memory = {}

        elif operation == "remove":
            key = context.get("key")
            self.working_memory.pop(key, None)

        return {
            "working_memory": dict(self.working_memory),
            "size": len(self.working_memory),
            "max_size": self.working_memory_size,
        }

    def get_recent_episodes(self, count: int = 10) -> List[Dict]:
        """API per ottenere episodi recenti"""
        return self.episodes[-count:]

    def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "episodes_stored": len(self.episodes),
            "semantic_memory_size": len(self.semantic_memory),
            "working_memory_items": len(self.working_memory),
            "last_access": self.last_access.isoformat(),
            "encoding_count": self.encoding_count,
            "recall_count": self.recall_count,
        }
