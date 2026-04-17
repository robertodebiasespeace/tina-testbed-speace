"""
Olfactory Sensor Protocol
Gas, VOC (Volatile Organic Compounds), sensori chimici

Versione: 1.0
Data: 2026-04-17
"""

import logging
import random
from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger("Olfactory-Sensor")


@dataclass
class AirQualityReading:
    """Lettura qualità aria"""
    reading_id: str
    timestamp: str
    voc_ppm: float
    co2_ppm: float
    aqi: int  # Air Quality Index (0-500)
    compounds_detected: List[str]


class OlfactorySensor:
    """
    Sensore olfattivo per Agente Organismico.
    Supporta: gas tossici, VOC, qualità aria.
    """

    def __init__(self, source: str = "simulated"):
        self.source = source
        self.voc_range = (0.0, 100.0)  # ppm
        self.co2_range = (300.0, 2000.0)  # ppm (typical indoor)
        self.last_reading: AirQualityReading = None
        self.version = "1.0"
        logger.info(f"OlfactorySensor initialized (source: {source})")

    def calculate_aqi(self, voc: float, co2: float) -> int:
        """
        Calcola Air Quality Index.
        EPA standard: 0-50 good, 51-100 moderate, 101-150 unhealthy for sensitive, etc.
        """
        # Simplified AQI calculation based on VOC and CO2
        if voc < 0.5 and co2 < 800:
            return int(random.uniform(0, 30))  # Good
        elif voc < 1.0 and co2 < 1000:
            return int(random.uniform(40, 70))  # Moderate
        elif voc < 2.0 and co2 < 1500:
            return int(random.uniform(80, 120))  # Unhealthy for sensitive
        else:
            return int(random.uniform(130, 180))  # Unhealthy

    def read_air_quality(self) -> AirQualityReading:
        """
        Legge qualità aria.
        In simulation restituisce valori random in range.
        """
        reading_id = f"olf_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        voc = random.uniform(*self.voc_range)
        co2 = random.uniform(*self.co2_range)
        aqi = self.calculate_aqi(voc, co2)

        compounds = []
        if voc > 0.5:
            compounds.append("ethanol")
        if voc > 1.0:
            compounds.append("acetone")
        if co2 > 1000:
            compounds.append("elevated_co2")

        reading = AirQualityReading(
            reading_id=reading_id,
            timestamp=datetime.now().isoformat(),
            voc_ppm=round(voc, 2),
            co2_ppm=round(co2, 1),
            aqi=aqi,
            compounds_detected=compounds
        )
        self.last_reading = reading
        return reading

    def get_health_recommendation(self, reading: AirQualityReading) -> str:
        """Genera raccomandazione salute"""
        if reading.aqi <= 50:
            return "air_quality_good"
        elif reading.aqi <= 100:
            return "ventilation_recommended"
        elif reading.aqi <= 150:
            return "sensitive_groups_should_limit_exposure"
        else:
            return "evacuate_or_wear_protection"


if __name__ == "__main__":
    sensor = OlfactorySensor("simulated")
    reading = sensor.read_air_quality()
    print(f"AQI: {reading.aqi} ({reading.voc_ppm} ppm VOC, {reading.co2_ppm} ppm CO2)")
