"""
Gustatory Sensor Protocol
Sensori chimici, pH, analisi sostanze

Versione: 1.0
Data: 2026-04-17
"""

import logging
import random
from typing import Dict, Any
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger("Gustatory-Sensor")


@dataclass
class ChemicalReading:
    """Lettura chimica"""
    reading_id: str
    timestamp: str
    ph_value: float
    concentration_ppm: float
    substance_type: str
    is_hazardous: bool


class GustatorySensor:
    """
    Sensore gustativo per Agente Organismico.
    Supporta: pH meter, sensori chimici specifici.
    """

    def __init__(self, source: str = "simulated"):
        self.source = source
        self.ph_range = (0.0, 14.0)
        self.concentration_range = (0.0, 1000.0)  # ppm
        self.last_reading: ChemicalReading = None
        self.version = "1.0"
        logger.info(f"GustatorySensor initialized (source: {source})")

    def read_chemical(self) -> ChemicalReading:
        """
        Legge valori chimici.
        In simulation restituisce valori random.
        """
        reading_id = f"gust_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        ph = random.uniform(*self.ph_range)
        concentration = random.uniform(*self.concentration_range)

        substance_type = "neutral"
        is_hazardous = False

        if ph < 4.0 or ph > 9.0:
            substance_type = "corrosive"
            is_hazardous = True
        elif concentration > 500:
            substance_type = "concentrated"
            is_hazardous = True

        reading = ChemicalReading(
            reading_id=reading_id,
            timestamp=datetime.now().isoformat(),
            ph_value=round(ph, 2),
            concentration_ppm=round(concentration, 1),
            substance_type=substance_type,
            is_hazardous=is_hazardous
        )
        self.last_reading = reading
        return reading

    def analyze_water_quality(self, reading: ChemicalReading) -> Dict[str, Any]:
        """Analisi qualità acqua"""
        if 6.5 <= reading.ph_value <= 8.5:
            ph_status = "optimal"
        elif 6.0 <= reading.ph_value <= 9.0:
            ph_status = "acceptable"
        else:
            ph_status = "out_of_range"

        return {
            "ph_status": ph_status,
            "ph_value": reading.ph_value,
            "concentration_ppm": reading.concentration_ppm,
            "is_hazardous": reading.is_hazardous,
            "recommendation": "safe" if not reading.is_hazardous else "handle_with_care"
        }


if __name__ == "__main__":
    sensor = GustatorySensor("simulated")
    reading = sensor.read_chemical()
    print(f"pH: {reading.ph_value}, Type: {reading.substance_type}")
