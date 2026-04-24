"""
SPEACE Meta-Neurone Dialogico v2.1 - Gemma3:12b
Contesto SPEACE ricco + Memoria + Ragionamento avanzato
"""

from typing import Dict, Any, List
from datetime import datetime
import json
import asyncio
import logging

logger = logging.getLogger("SelfDialogueAgent")

class SelfDialogueAgent:
    def __init__(self):
        self.name = "self_dialogue_agent"
        self.version = "2.1"
        self.bridge = None
        self.learning_core = None
        self.history: List[Dict] = []
        self.max_history = 30
        self.model = "gemma3:12b"
        self.ollama_available = False

    def set_bridge(self, bridge):
        self.bridge = bridge
        if hasattr(bridge, 'learning_core') and bridge.learning_core:
            self.learning_core = bridge.learning_core
            print("✅ Learning Core collegato al Meta-Neurone")

        try:
            import ollama
            self.ollama_available = True
            print(f"✅ Ollama + {self.model} attivo")
        except ImportError:
            print("⚠️ ollama library non trovata")

    async def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        query = context.get("query", "").strip() or "Qual è il tuo stato attuale e cosa dovremmo migliorare?"

        state = self._collect_rich_state()
        
        if self.ollama_available:
            response = await self._ollama_reasoning(query, state)
        else:
            response = self._fallback(query, state)

        suggestion = self._generate_suggestion(state)

        self._add_to_history(query, response, suggestion, state)

        if self.learning_core:
            self.learning_core.learn(
                {"c_index": state["c_index"], "history": len(self.history)},
                0.85 + (state["c_index"] * 0.15),
                {"agent": "self_dialogue"}
            )

        return {
            "status": "dialogue_complete",
            "agent": "Meta-Neurone Dialogico v2.1",
            "response": response,
            "suggestion": suggestion,
            "confidence": 0.90,
            "learning_core_connected": self.learning_core is not None,
            "ollama_connected": self.ollama_available,
            "model": self.model
        }

    def _collect_rich_state(self) -> Dict:
        state = {
            "c_index": 0.80,
            "cycle_count": 0,
            "compartments_active": 12,
            "graph_engine": "active",
            "swarm": "initialized"
        }
        if self.bridge:
            state["c_index"] = getattr(self.bridge, 'get_c_index', lambda: 0.80)()
            state["cycle_count"] = getattr(self.bridge, 'cycle_count', 0)
            state["compartments_active"] = len(getattr(self.bridge, 'compartments', {}))
        return state

    async def _ollama_reasoning(self, query: str, state: Dict) -> str:
        import ollama
        system_prompt = f"""Sei il Meta-Neurone Dialogico di SPEACE, parte del Rigene Project.
Stato attuale: C-index {state['c_index']:.3f}, {state['compartments_active']} comparti, {state['cycle_count']} cicli.
Ragiona in modo profondo, autocritico, propositivo e allineato con armonia, rigenerazione e evoluzione."""

        try:
            resp = await asyncio.to_thread(
                ollama.chat,
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                options={"temperature": 0.7, "num_ctx": 8192}
            )
            return resp['message']['content'].strip()
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            return self._fallback(query, state)

    def _fallback(self, query: str, state: Dict) -> str:
        return f"C-index {state['c_index']:.3f}. Il sistema è stabile ma ha margini di miglioramento nell'integrazione tra comparti."

    def _generate_suggestion(self, state: Dict) -> str:
        return "Eseguire experience replay + mutazione epigenetica per aumentare la plasticità del grafo."

    def _add_to_history(self, query: str, response: str, suggestion: str, state: Dict):
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response[:700],
            "c_index": state["c_index"]
        })
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def get_status(self):
        return {
            "name": self.name,
            "version": self.version,
            "model": self.model,
            "ollama_connected": self.ollama_available,
            "learning_core_connected": self.learning_core is not None,
            "history_length": len(self.history),
            "status": "active"
        }
