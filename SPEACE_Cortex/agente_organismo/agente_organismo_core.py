"""
Agente Organismico Core - SPEACE Physical Extension
SMFOI-KERNEL Extension per interazione con mondo fisico

Versione: 1.0
Data: 2026-04-17
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Agente-Organismo")


class SensorType(Enum):
    """Tipi di sensori supportati"""
    VISUAL = "visual"
    ACOUSTIC = "acoustic"
    THERMAL = "thermal"
    OLFACTORY = "olfactory"
    GUSTATORY = "gustatory"
    TACTILE = "tactile"


class SurvivalLevel(Enum):
    """Livelli dello Survival & Evolution Stack"""
    LV0_REACTIVE = "Lv0: Reactive (base)"
    LV1_ADAPTIVE = "Lv1: Adaptive (learning)"
    LV2_PROACTIVE = "Lv2: Proactive (goal-seeking)"
    LV3_AUTO_MODIFYING = "Lv3: Auto-modifying"
    LV4_PHYSICAL_INTERACTION = "Lv4: Physical Interaction (NEW)"


@dataclass
class SensorReading:
    """Lettura singola sensore"""
    sensor_type: SensorType
    value: Any
    unit: str
    timestamp: str
    confidence: float = 1.0
    location: Optional[Dict[str, float]] = None


@dataclass
class PhysicalAction:
    """Azione fisica proposta"""
    action_type: str
    target: str
    parameters: Dict[str, Any]
    requires_approval: bool = True
    risk_level: str = "high"
    estimated_impact: str = ""


@dataclass
class OrganismState:
    """Stato interno Agente Organismico"""
    smfoi_extended: bool = True
    sensors_active: List[SensorType] = field(default_factory=list)
    last_readings: List[SensorReading] = field(default_factory=list)
    pending_actions: List[PhysicalAction] = field(default_factory=list)
    survival_level: SurvivalLevel = SurvivalLevel.LV4_PHYSICAL_INTERACTION
    iot_connected: bool = False
    physical_presence: str = "edge_device"


class AgenteOrganismoCore:
    """
    Core dell'Agente Organismico.
    Estende SMFOI-KERNEL per sensing e attuazione fisica.
    """

    def __init__(self, smfoi_kernel=None):
        self.state = OrganismState()
        self.smfoi = smfoi_kernel
        self.version = "1.0"
        logger.info("Agente Organismico Core initialized (v1.0)")

    # === SMFOI-KERNEL Extension ===

    def smfoi_step3_extended(self, input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Step 3 Extended: Push Detection include segnali IoT
        """
        pushes = []

        # Standard pushes from SMFOI
        if "user_request" in input_data:
            pushes.append({
                "type": "user_request",
                "source": "human",
                "payload": input_data["user_request"],
                "priority": "high"
            })

        # NEW: IoT sensor pushes
        if "sensor_data" in input_data:
            for reading in input_data["sensor_data"]:
                sensor_type = reading.get("type", "unknown")
                pushes.append({
                    "type": "iot_sensor",
                    "source": reading.get("source", "unknown"),
                    "sensor_type": sensor_type,
                    "payload": reading,
                    "priority": reading.get("priority", "medium"),
                    "confidence": reading.get("confidence", 1.0)
                })

        # NEW: Physical anomalies
        if "physical_anomalies" in input_data:
            for anomaly in input_data["physical_anomalies"]:
                pushes.append({
                    "type": "physical_anomaly",
                    "source": "environment",
                    "payload": anomaly,
                    "priority": "critical",
                    "requires_action": True
                })

        return pushes

    def smfoi_step4_extended(self) -> Dict[str, Any]:
        """
        Step 4 Extended: Survival Stack con Lv4 Physical Interaction
        """
        stack = {
            "level_0_reactive": {
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
            },
            "level_4_physical_interaction": {
                "description": "Physical world interaction (NEW)",
                "trigger": "iot_sensor_anomaly_or_opportunity",
                "execution": "plan_physical_action_via_safeproactive",
                "requires_approval": True,
                "risk_level": "high",
                "example": "Activate robot arm, adjust HVAC, trigger drone"
            }
        }
        return stack

    def smfoi_step5_extended(self, push_data: Dict[str, Any]) -> Optional[PhysicalAction]:
        """
        Step 5 Extended: Output include attuatori
        """
        sensor_type = push_data.get("sensor_type", "unknown")

        # Map sensor type to potential action
        action_mapping = {
            "thermal": {
                "action_type": "temperature_control",
                "description": "Adjust HVAC based on thermal reading",
                "approval_required": True
            },
            "olfactory": {
                "action_type": "air_quality_control",
                "description": "Trigger air purification",
                "approval_required": True
            },
            "visual": {
                "action_type": "surveillance_alert",
                "description": "Alert based on visual anomaly",
                "approval_required": False  # Can be automatic
            }
        }

        if sensor_type in action_mapping:
            action_def = action_mapping[sensor_type]
            return PhysicalAction(
                action_type=action_def["action_type"],
                target=push_data.get("source", "unknown"),
                parameters={"sensor_data": push_data},
                requires_approval=action_def["approval_required"],
                risk_level="high" if action_def["approval_required"] else "medium",
                estimated_impact=action_def["description"]
            )

        return None

    # === Sensor Management ===

    def register_sensor(self, sensor_type: SensorType, config: Dict[str, Any]):
        """Registra un nuovo sensore"""
        self.state.sensors_active.append(sensor_type)
        logger.info(f"Sensor registered: {sensor_type.value}")

    def get_simulated_reading(self, sensor_type: SensorType) -> SensorReading:
        """
        Genera lettura simulata per testing.
        In produzione, questo leggerà da sensori reali via IoT interface.
        """
        import random

        # Simulation data per tipo sensore
        simulations = {
            SensorType.VISUAL: {"value": "frame_001", "unit": "image/jpeg"},
            SensorType.ACOUSTIC: {"value": round(random.uniform(40, 80), 2), "unit": "dB"},
            SensorType.THERMAL: {"value": round(random.uniform(18, 28), 2), "unit": "°C"},
            SensorType.OLFACTORY: {"value": round(random.uniform(0, 100), 2), "unit": "VOC_ppm"},
            SensorType.GUSTATORY: {"value": round(random.uniform(0, 14), 2), "unit": "pH"},
            SensorType.TACTILE: {"value": round(random.uniform(0, 10), 2), "unit": "kg/cm²"},
        }

        data = simulations.get(sensor_type, {"value": 0, "unit": "unknown"})

        return SensorReading(
            sensor_type=sensor_type,
            value=data["value"],
            unit=data["unit"],
            timestamp=datetime.now().isoformat(),
            confidence=random.uniform(0.85, 0.99),
            location={"lat": 41.9028, "lon": 12.4964}  # Rome example
        )

    def collect_all_sensor_data(self) -> List[SensorReading]:
        """Raccoglie dati da tutti i sensori attivi (simulati)"""
        readings = []
        for sensor_type in self.state.sensors_active:
            reading = self.get_simulated_reading(sensor_type)
            readings.append(reading)
        self.state.last_readings = readings
        return readings

    # === Main Processing Loop ===

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ciclo principale di processing.
        Estende SMFOI con Physical Interaction.
        """
        logger.info("=== Agente Organismo Processing ===")

        # Step 3 Extended: Push Detection
        pushes = self.smfoi_step3_extended(input_data)

        # Step 4 Extended: Survival Stack
        survival_stack = self.smfoi_step4_extended()

        # Determine active level
        active_level = "level_4_physical_interaction" if any(
            p.get("type") == "iot_sensor" for p in pushes
        ) else "level_2_proactive"

        # Step 5 Extended: Generate physical action if needed
        physical_action = None
        for push in pushes:
            if push.get("type") == "iot_sensor":
                action = self.smfoi_step5_extended(push)
                if action:
                    physical_action = action
                    break

        # Collect sensor data
        sensor_readings = self.collect_all_sensor_data()

        return {
            "status": "processed",
            "version": self.version,
            "pushes_detected": len(pushes),
            "survival_stack_active": active_level,
            "physical_action_proposed": physical_action.__dict__ if physical_action else None,
            "sensor_readings_count": len(sensor_readings),
            "sensors_active": [s.value for s in self.state.sensors_active],
            "timestamp": datetime.now().isoformat()
        }


def create_agente_organismo(smfoi_kernel=None) -> AgenteOrganismoCore:
    """Factory function"""
    return AgenteOrganismoCore(smfoi_kernel)


if __name__ == "__main__":
    # Test dell'Agente Organismico
    print("Agente Organismico v1.0 - Test")

    agente = create_agente_organismo()

    # Register sensors
    for sensor_type in SensorType:
        agente.register_sensor(sensor_type, {})

    # Process test input
    test_input = {
        "user_request": "Monitora ambiente",
        "sensor_data": [
            {"type": "thermal", "source": "sensor_01", "value": 25.5, "priority": "medium"},
            {"type": "olfactory", "source": "sensor_02", "value": 45.2, "priority": "medium"}
        ]
    }

    result = agente.process(test_input)
    print(json.dumps(result, indent=2, default=str))
