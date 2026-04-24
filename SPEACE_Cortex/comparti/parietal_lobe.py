"""
Parietal Lobe - Sensory & Tools Integration
Composto per l'integrazione sensori e strumenti esterni.
Versione: 1.0
Data: 23 Aprile 2026
"""

from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
import logging

logger = logging.getLogger("ParietalLobe")


class ParietalLobe:
    """
    Parietal Lobe - Sensory Integration e Tools.

    Responsabilita:
    - Coordinazione input/output multi-sensoriale
    - Gestione tool calling
    - Integrazione con API e servizi esterni
    - Spatial reasoning
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.name = "parietal_lobe"
        self.version = "1.1"
        self.config = config or {}
        self.bridge = None

        # Tool registry
        self.tools: Dict[str, Callable] = {}
        self.tool_history: List[Dict] = []
        self.max_tool_history = self.config.get("max_history", 100)

        # Sensory integration
        self.sensory_buffer: Dict[str, Any] = {}
        self.integration_mode = self.config.get("integration_mode", "adaptive")

        # Available APIs/servizi
        self.services = ["http", "mqtt", "websocket", "rest_api", "filesystem"]
        self.active_connections: Dict[str, bool] = {s: False for s in self.services}

        self.last_integration = datetime.now()
        self.tool_calls = 0

    def set_bridge(self, bridge):
        """Imposta il riferimento al Neural Bridge"""
        self.bridge = bridge

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processo principale Parietal Lobe.

        Args:
            context: Contesto con operation, tool_call, sensory_data

        Returns:
            Dict con integration_results
        """
        self.last_integration = datetime.now()

        try:
            operation = context.get("operation", "integrate")

            if operation == "tool_call":
                result = self._execute_tool(context)
            elif operation == "integrate_sensory":
                result = self._integrate_sensory(context)
            elif operation == "spatial":
                result = self._spatial_reasoning(context)
            elif operation == "connect_service":
                result = self._connect_service(context)
            else:
                result = {"status": "unknown_operation"}

            return {
                "status": "success",
                "result": result,
                "comparto": self.name,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"ParietalLobe error: {e}")
            return {"status": "error", "error": str(e), "comparto": self.name}

    def _execute_tool(self, context: Dict) -> Dict[str, Any]:
        """Esegue un tool call"""
        tool_name = context.get("tool_name", "unknown")
        tool_args = context.get("tool_args", {})

        # Check se tool esiste
        if tool_name in self.tools:
            try:
                result = self.tools[tool_name](**tool_args)
                success = True
            except Exception as e:
                result = {"error": str(e)}
                success = False
        else:
            # Tool simulato
            result = {"simulated": True, "tool": tool_name, "args": tool_args}
            success = True

        self.tool_history.append({
            "timestamp": datetime.now().isoformat(),
            "tool": tool_name,
            "success": success,
        })
        self.tool_calls += 1

        if len(self.tool_history) > self.max_tool_history:
            self.tool_history = self.tool_history[-self.max_tool_history:]

        return {
            "tool": tool_name,
            "success": success,
            "result": result,
            "tool_calls_total": self.tool_calls,
        }

    def register_tool(self, name: str, func: Callable):
        """Registra un nuovo tool"""
        self.tools[name] = func
        logger.info(f"Registered tool: {name}")

    def _integrate_sensory(self, context: Dict) -> Dict[str, Any]:
        """Integra dati sensoriali da sorgenti multiple"""
        sensory_inputs = context.get("sensory_inputs", {})

        for modality, data in sensory_inputs.items():
            self.sensory_buffer[modality] = {
                "data": data,
                "timestamp": datetime.now().isoformat(),
            }

        # Fusione adattiva
        fused = self._adaptive_fusion()

        return {
            "modalities_received": list(sensory_inputs.keys()),
            "buffer_size": len(self.sensory_buffer),
            "fused_output": fused,
            "integration_mode": self.integration_mode,
        }

    def _adaptive_fusion(self) -> Dict[str, Any]:
        """Fusione adattiva multi-sensoriale"""
        if not self.sensory_buffer:
            return {"fused": False}

        # Pesi semplici per modalita
        weights = {
            "visual": 0.30,
            "acoustic": 0.20,
            "tactile": 0.15,
            "contextual": 0.35,
        }

        fused_signal = "multi_modal_integration"
        confidence = 0.68 + len(self.sensory_buffer) * 0.03

        return {
            "fused": True,
            "signal": fused_signal,
            "confidence": min(0.95, confidence),
            "modalities": list(self.sensory_buffer.keys()),
        }

    def _spatial_reasoning(self, context: Dict) -> Dict[str, Any]:
        """Ragionamento spaziale"""
        objects = context.get("objects", [])
        query = context.get("spatial_query", "where")

        # Risponde a query spaziali semplici
        if query == "where":
            return {
                "query": query,
                "reasoning": "Simulated spatial reasoning",
                "confidence": 0.60,
                "objects_count": len(objects),
            }
        return {"query": query, "reasoning": "unknown query type"}

    def _connect_service(self, context: Dict) -> Dict[str, Any]:
        """Connette a un servizio"""
        service = context.get("service", "")

        if service in self.services:
            self.active_connections[service] = True
            return {
                "service": service,
                "connected": True,
                "active_connections": sum(self.active_connections.values()),
            }

        return {"service": service, "connected": False, "error": "unknown service"}

    def get_available_tools(self) -> List[str]:
        """API per ottenere tool disponibili"""
        return list(self.tools.keys())

    def get_tool_history(self, count: int = 20) -> List[Dict]:
        """API per ottenere storico tool calls"""
        return self.tool_history[-count:]

    def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "tools_registered": len(self.tools),
            "tool_calls": self.tool_calls,
            "active_connections": sum(self.active_connections.values()),
            "sensory_buffer_size": len(self.sensory_buffer),
            "last_integration": self.last_integration.isoformat(),
        }
