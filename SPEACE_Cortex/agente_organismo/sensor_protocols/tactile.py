"""
Tactile Sensor Protocol
Sensori pressione, texture, forza, contatto

Versione: 1.0
Data: 2026-04-17
"""

import logging
import random
from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger("Tactile-Sensor")


@dataclass
class TactileReading:
    """Lettura tattile"""
    reading_id: str
    timestamp: str
    pressure_kg_cm2: float
    texture: str
    temperature_celsius: float
    contact_points: int


class TactileSensor:
    """
    Sensore tattile per Agente Organismico.
    Supporta: array pressione, sensori texture, termici接触.
    """

    def __init__(self, source: str = "simulated"):
        self.source = source
        self.pressure_range = (0.0, 20.0)  # kg/cm²
        self.temperature_range = (15.0, 45.0)  # Celsius
        self.last_reading: TactileReading = None
        self.version = "1.0"
        logger.info(f"TactileSensor initialized (source: {source})")

    def read_pressure(self) -> TactileReading:
        """
        Legge valori tattili.
        In simulation restituisce valori random.
        """
        reading_id = f"tact_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        pressure = random.uniform(*self.pressure_range)
        temperature = random.uniform(*self.temperature_range)

        textures = ["smooth", "rough", "textured", "sticky", "slippery"]
        texture = random.choice(textures)

        contact_points = random.randint(1, 5)

        reading = TactileReading(
            reading_id=reading_id,
            timestamp=datetime.now().isoformat(),
            pressure_kg_cm2=round(pressure, 3),
            texture=texture,
            temperature_celsius=round(temperature, 1),
            contact_points=contact_points
        )
        self.last_reading = reading
        return reading

    def detect_slip_risk(self, reading: TactileReading) -> Dict[str, Any]:
        """Rileva rischio scivolamento"""
        slip_risk = "low"
        if reading.texture == "slippery" and reading.pressure_kg_cm2 < 1.0:
            slip_risk = "high"
        elif reading.texture == "smooth" and reading.pressure_kg_cm2 < 2.0:
            slip_risk = "medium"

        return {
            "slip_risk": slip_risk,
            "pressure": reading.pressure_kg_cm2,
            "texture": reading.texture,
            "recommendation": "caution" if slip_risk != "low" else "normal"
        }


if __name__ == "__main__":
    sensor = TactileSensor("simulated")
    reading = sensor.read_pressure()
    print(f"Pressure: {reading.pressure_kg_cm2} kg/cm², Texture: {reading.texture}")
