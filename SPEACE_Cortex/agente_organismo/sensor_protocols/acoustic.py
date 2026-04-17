"""
Acoustic Sensor Protocol
Microfoni, sonar, analisi audio

Versione: 1.0
Data: 2026-04-17
"""

import logging
import random
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger("Acoustic-Sensor")


@dataclass
class AudioSample:
    """Campione audio"""
    sample_id: str
    timestamp: str
    duration_ms: int
    sample_rate: int
    amplitude_db: float
    frequency_hz: Optional[float] = None


class AcousticSensor:
    """
    Sensore acustico per Agente Organismico.
    Supporta: microfoni, array microfonici, sonar.
    """

    def __init__(self, source: str = "simulated"):
        self.source = source
        self.sample_rate = 44100
        self.channels = 1
        self.amplitude_range = (20, 85)  # dB typical range
        self.last_sample: Optional[AudioSample] = None
        self.version = "1.0"
        logger.info(f"AcousticSensor initialized (source: {source})")

    def capture_sample(self, duration_ms: int = 1000) -> AudioSample:
        """
        Cattura campione audio.
        In simulation restituisce valori random.
        """
        sample_id = f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        if self.source == "simulated":
            amplitude = random.uniform(*self.amplitude_range)
            return AudioSample(
                sample_id=sample_id,
                timestamp=datetime.now().isoformat(),
                duration_ms=duration_ms,
                sample_rate=self.sample_rate,
                amplitude_db=round(amplitude, 2),
                frequency_hz=random.uniform(50, 4000)
            )

        raise NotImplementedError("Real capture not implemented")

    def analyze_frequency(self, sample: AudioSample) -> Dict[str, Any]:
        """Analisi frequenza dominante"""
        return {
            "dominant_frequency": sample.frequency_hz,
            "frequency_band": "low" if sample.frequency_hz < 300 else "mid" if sample.frequency_hz < 3000 else "high",
            "amplitude_db": sample.amplitude_db
        }

    def detect_anomalies(self, sample: AudioSample) -> List[str]:
        """Rileva anomalie sonore"""
        anomalies = []
        if sample.amplitude_db > 80:
            anomalies.append("high_amplitude_warning")
        if sample.frequency_hz and sample.frequency_hz > 3500:
            anomalies.append("ultrasonic_detected")
        return anomalies

    def get_environment_classification(self, sample: AudioSample) -> str:
        """Classifica ambiente basato su caratteristiche audio"""
        if sample.amplitude_db < 30:
            return "quiet_indoor"
        elif sample.amplitude_db < 60:
            return "normal_environment"
        elif sample.amplitude_db < 80:
            return "noisy_environment"
        else:
            return "very_loud_warning"


if __name__ == "__main__":
    sensor = AcousticSensor("simulated")
    sample = sensor.capture_sample()
    print(f"Amplitude: {sample.amplitude_db} dB")
