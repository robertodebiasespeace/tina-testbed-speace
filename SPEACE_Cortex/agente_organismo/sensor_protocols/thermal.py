"""
Thermal Sensor Protocol
Infrarossi, sensori temperatura corporea, termocamere

Versione: 1.0
Data: 2026-04-17
"""

import logging
import random
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger("Thermal-Sensor")


@dataclass
class ThermalReading:
    """Lettura termica"""
    reading_id: str
    timestamp: str
    temperature_celsius: float
    humidity_percent: Optional[float]
    sensor_type: str
    is_anomaly: bool = False


class ThermalSensor:
    """
    Sensore termico per Agente Organismico.
    Supporta: IR temperature, termocoppie, termistori.
    """

    def __init__(self, source: str = "simulated"):
        self.source = source
        self.temperature_range = (15.0, 35.0)  # Celsius
        self.humidity_range = (30.0, 80.0)  # Percent
        self.last_reading: Optional[ThermalReading] = None
        self.version = "1.0"
        logger.info(f"ThermalSensor initialized (source: {source})")

    def read_temperature(self) -> ThermalReading:
        """
        Legge temperatura attuale.
        In simulation restituisce valore random in range.
        """
        reading_id = f"thermal_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        temperature = random.uniform(*self.temperature_range)
        humidity = random.uniform(*self.humidity_range)

        is_anomaly = temperature > 30.0 or temperature < 18.0

        reading = ThermalReading(
            reading_id=reading_id,
            timestamp=datetime.now().isoformat(),
            temperature_celsius=round(temperature, 2),
            humidity_percent=round(humidity, 1),
            sensor_type="thermistor",
            is_anomaly=is_anomaly
        )
        self.last_reading = reading
        return reading

    def detect_hotspots(self) -> list:
        """
        Rileva hotspot termici (persone, fuoco, macchinari).
        In implementation reale: FLIR image processing.
        """
        if self.source == "simulated":
            return [
                {"location": "center", "temperature": 37.0, "type": "body_heat"},
                {"location": "corner", "temperature": 45.0, "type": "electronics"}
            ]
        return []

    def analyze_thermal_map(self) -> Dict[str, Any]:
        """
        Analisi completa mappa termica.
        """
        reading = self.read_temperature()
        hotspots = self.detect_hotspots()

        return {
            "reading_id": reading.reading_id,
            "timestamp": reading.timestamp,
            "ambient_temperature": reading.temperature_celsius,
            "humidity": reading.humidity_percent,
            "hotspots_count": len(hotspots),
            "hotspots": hotspots,
            "is_anomaly": reading.is_anomaly,
            "recommendation": "investigate" if reading.is_anomaly else "normal"
        }


if __name__ == "__main__":
    sensor = ThermalSensor("simulated")
    result = sensor.analyze_thermal_map()
    print(f"Ambient: {result['ambient_temperature']}°C, Hotspots: {result['hotspots_count']}")
