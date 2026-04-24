"""
Temporal Lobe - Language, Crypto & Market Analysis
Composto per elaborazione temporale, linguaggio e analisi di mercato.
Versione: 1.0
Data: 23 Aprile 2026
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("TemporalLobe")


class TemporalLobe:
    """
    Temporal Lobe - Language Processing e Market Analysis.

    Responsabilita:
    - Elaborazione e comprensione del linguaggio
    - Analisi temporalmente ordinata
    - Crypto e Market data processing
    - Sequence recognition
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.name = "temporal_lobe"
        self.version = "1.1"
        self.config = config or {}
        self.bridge = None

        # Market data cache
        self.market_data: Dict[str, Any] = {
            "crypto": {},
            "stocks": {},
            "forex": {},
        }
        self.market_history: List[Dict] = []

        # Language processing
        self.language_model = "local_embeddings"
        self.context_window = self.config.get("context_window", 2048)

        # Temporal patterns
        self.patterns_detected: List[Dict] = []
        self.last_analysis = datetime.now()

    def set_bridge(self, bridge):
        """Imposta il riferimento al Neural Bridge"""
        self.bridge = bridge

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processo principale Temporal Lobe.

        Args:
            context: Contesto con operation e dati

        Returns:
            Dict con analysis_results
        """
        self.last_analysis = datetime.now()

        try:
            operation = context.get("operation", "analyze")

            if operation == "analyze_market":
                result = self._analyze_market(context)
            elif operation == "analyze_language":
                result = self._analyze_language(context)
            elif operation == "detect_patterns":
                result = self._detect_temporal_patterns(context)
            elif operation == "predict":
                result = self._predict_sequence(context)
            else:
                result = {"status": "unknown_operation"}

            return {
                "status": "success",
                "result": result,
                "comparto": self.name,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"TemporalLobe error: {e}")
            return {"status": "error", "error": str(e), "comparto": self.name}

    def _analyze_market(self, context: Dict) -> Dict[str, Any]:
        """Analizza dati di mercato"""
        market_type = context.get("market_type", "crypto")
        symbols = context.get("symbols", ["BTC", "ETH"])

        results = {}
        for symbol in symbols:
            # Simula dati di mercato
            results[symbol] = {
                "price": self._get_simulated_price(symbol),
                "change_24h": round((hash(symbol) % 10 - 5) * 0.5, 2),
                "volume": hash(symbol) % 1000000000,
                "trend": "bullish" if hash(symbol) % 2 == 0 else "bearish",
                "confidence": 0.72,
            }

        # Aggiorna cache
        self.market_data[market_type] = results
        self.market_history.append({
            "timestamp": datetime.now().isoformat(),
            "data": results,
        })

        # Mantieni ultimi 100
        if len(self.market_history) > 100:
            self.market_history = self.market_history[-100:]

        return {
            "market_type": market_type,
            "analysis": results,
            "symbols_analyzed": len(symbols),
            "trend_summary": self._get_trend_summary(results),
        }

    def _get_simulated_price(self, symbol: str) -> float:
        """Simula prezzo per symbol"""
        base_prices = {
            "BTC": 67450.0,
            "ETH": 3520.0,
            "SOL": 145.0,
            "XRP": 0.52,
        }
        return base_prices.get(symbol, 100.0)

    def _get_trend_summary(self, results: Dict) -> str:
        """Genera summary trend"""
        bullish = sum(1 for v in results.values() if v.get("trend") == "bullish")
        total = len(results)
        ratio = bullish / total if total > 0 else 0.5

        if ratio > 0.7:
            return "STRONG_BULLISH"
        elif ratio > 0.5:
            return "MODERATE_BULLISH"
        elif ratio > 0.3:
            return "MODERATE_BEARISH"
        else:
            return "STRONG_BEARISH"

    def _analyze_language(self, context: Dict) -> Dict[str, Any]:
        """Analizza contenuto linguistico"""
        text = context.get("text", "")

        # Analisi molto semplificata
        words = text.split()
        return {
            "text": text[:100] + "..." if len(text) > 100 else text,
            "word_count": len(words),
            "entities": self._extract_simple_entities(text),
            "sentiment": self._simple_sentiment(text),
            "language": "en",
            "confidence": 0.68,
        }

    def _extract_simple_entities(self, text: str) -> List[str]:
        """Estrazione semplice entita (keywords capitalizzate)"""
        return [w for w in text.split() if w and w[0].isupper() and len(w) > 2][:5]

    def _simple_sentiment(self, text: str) -> str:
        """Sentiment analysis semplificata"""
        positive = ["good", "great", "excellent", "bullish", "up", "profit", "gain"]
        negative = ["bad", "poor", "bearish", "down", "loss", "risk", "danger"]

        text_lower = text.lower()
        pos_count = sum(1 for w in positive if w in text_lower)
        neg_count = sum(1 for w in negative if w in text_lower)

        if pos_count > neg_count:
            return "positive"
        elif neg_count > pos_count:
            return "negative"
        return "neutral"

    def _detect_temporal_patterns(self, context: Dict) -> Dict[str, Any]:
        """Rileva patterns temporali nella history"""
        data = self.market_history[-20:]  # Ultimi 20

        patterns = []
        if len(data) >= 5:
            # Simple pattern: consecutive ups/downs
            last_5 = [d["data"] for d in data[-5:]]
            trends = [list(d.values())[0].get("trend") for d in last_5]

            if len(set(trends)) == 1:
                patterns.append({
                    "type": "consecutive_trend",
                    "direction": trends[0],
                    "duration": len(trends),
                    "confidence": 0.75,
                })

        return {
            "patterns": patterns,
            "data_points_analyzed": len(data),
            "pattern_count": len(patterns),
        }

    def _predict_sequence(self, context: Dict) -> Dict[str, Any]:
        """Predice prossimo valore in sequenza"""
        sequence = context.get("sequence", [])

        if len(sequence) < 3:
            return {"prediction": None, "confidence": 0}

        # Simple linear extrapolation
        diffs = [sequence[i+1] - sequence[i] for i in range(len(sequence)-1)]
        avg_diff = sum(diffs) / len(diffs) if diffs else 0

        prediction = sequence[-1] + avg_diff
        confidence = min(0.9, 0.5 + len(sequence) * 0.05)

        return {
            "prediction": round(prediction, 2),
            "confidence": confidence,
            "method": "linear_extrapolation",
            "sequence_length": len(sequence),
        }

    def get_market_status(self) -> Dict[str, Any]:
        """API per ottenere status mercato"""
        return {
            "crypto": self.market_data.get("crypto", {}),
            "history_points": len(self.market_history),
            "last_analysis": self.last_analysis.isoformat(),
        }

    def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "market_data_symbols": sum(len(v) for v in self.market_data.values()),
            "history_points": len(self.market_history),
            "patterns_detected": len(self.patterns_detected),
            "last_analysis": self.last_analysis.isoformat(),
        }
