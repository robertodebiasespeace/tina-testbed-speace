"""
Perception Module - Sensori, API, IoT Fetches
Composto per l'elaborazione degli input sensoriali e delle API.
Versione: 1.0
Data: 23 Aprile 2026
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger("PerceptionModule")


class PerceptionModule:
    """
    Perception Module - Elabora input da sensori, API esterne, IoT.

    Responsabilita:
    - Raccolta dati da sensori (visual, acoustic, tactile, thermal, gustatory, olfactory)
    - Fetch da API esterne (crypto, market, weather, news)
    - Aggregazione e normalizzazione sensory input
    - Gesture/intent recognition
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.name = "perception_module"
        self.version = "1.0"
        self.config = config or {}
        self.bridge = None
        self.sensors_enabled = self.config.get("sensors", [
            "visual", "acoustic", "tactile", "thermal", "gustatory", "olfactory"
        ])
        self.apis_enabled = self.config.get("apis", [
            "crypto", "weather", "news", "market"
        ])
        self.last_perception = datetime.now()
        self.perception_count = 0
        self.raw_inputs: List[Dict] = []
        self.fused_perception: Optional[Dict] = None

    def set_bridge(self, bridge):
        """Imposta il riferimento al Neural Bridge"""
        self.bridge = bridge

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processo principale di percezione.

        Args:
            context: Contesto con richieste specifiche

        Returns:
            Dict con perception_results, confidence, sensory_data
        """
        self.last_perception = datetime.now()
        self.perception_count += 1

        try:
            # Identifica tipo di percezione richiesta
            perception_type = context.get("perception_type", "api")

            if perception_type == "sensor":
                result = self._process_sensor_input(context)
            elif perception_type == "api":
                result = self._process_api_input(context)
            elif perception_type == "fused":
                result = self._process_fused_input(context)
            else:
                result = self._process_generic(context)

            self.fused_perception = result
            return {
                "status": "success",
                "perception": result,
                "perception_type": perception_type,
                "comparto": self.name,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"PerceptionModule error: {e}")
            return {"status": "error", "error": str(e), "comparto": self.name}

    def _process_sensor_input(self, context: Dict) -> Dict[str, Any]:
        """Processa input da sensori reali o simulati"""
        sensor_type = context.get("sensor_type", "all")
        return {
            "sensor_type": sensor_type,
            "data": {"simulated": True, "sensor": sensor_type},
            "confidence": 0.7,
            "raw_signal": f"sensor_{sensor_type}_data",
        }

    def _process_api_input(self, context: Dict) -> Dict[str, Any]:
        """Processa input da API esterne"""
        api_type = context.get("api_type", "generic")
        api_data = self._fetch_api_data(api_type)
        return {
            "api_type": api_type,
            "data": api_data,
            "confidence": 0.8,
            "source": f"{api_type}_api",
        }

    def _fetch_api_data(self, api_type: str) -> Dict[str, Any]:
        """Simula fetch da API"""
        api_map = {
            "crypto": {"btc_price": 67450, "eth_price": 3520, "source": "simulated"},
            "weather": {"temp": 22, "condition": "sunny", "source": "simulated"},
            "news": {"headlines": ["SPEACE evolves", "AI regulation"], "source": "simulated"},
            "market": {"sp500": 5180, "nasdaq": 16420, "source": "simulated"},
        }
        return api_map.get(api_type, {"status": "unknown_api"})

    def _process_fused_input(self, context: Dict) -> Dict[str, Any]:
        """Fonde input multi-sensoriale"""
        return {
            "fusion_type": "multimodal",
            "data": {
                "visual": {"confidence": 0.75},
                "acoustic": {"confidence": 0.70},
                "contextual": {"confidence": 0.82},
            },
            "fused_confidence": 0.76,
            "integrated_signal": "multimodal_percept",
        }

    def _process_generic(self, context: Dict) -> Dict[str, Any]:
        """Processo generico senza specifica"""
        return {
            "data": context.get("input_data", {}),
            "confidence": 0.6,
            "type": "generic_perception",
        }

    # === Sensori specifici ===

    def process_visual(self, image_data: Any) -> Dict[str, Any]:
        """Processa input visivo"""
        return {
            "sensor": "visual",
            "processed": True,
            "features": {"objects": [], "scene": "unknown"},
            "confidence": 0.7,
        }

    def process_acoustic(self, audio_data: Any) -> Dict[str, Any]:
        """Processa input acustico"""
        return {
            "sensor": "acoustic",
            "processed": True,
            "features": {"speech": False, "ambient": True},
            "confidence": 0.65,
        }

    # === Status ===

    def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "sensors_enabled": len(self.sensors_enabled),
            "apis_enabled": len(self.apis_enabled),
            "last_perception": self.last_perception.isoformat(),
            "perception_count": self.perception_count,
        }
