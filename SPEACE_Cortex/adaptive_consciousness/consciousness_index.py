"""
Consciousness Index (C-index) Calculator

Composite metric combining:
- Φ (phi): Integrated Information Theory metric
- W-activation: Global Workspace Theory metric
- A-complexity: Adaptive Metacognition metric

C-index = α*Φ + β*W-activation + γ*A-complexity

Version: 1.0
Date: 2026-04-18
"""

import numpy as np
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ConsciousnessIndex")


@dataclass
class CIndexComponents:
    """Components of the C-index."""
    phi: float = 0.0
    w_activation: float = 0.0
    a_complexity: float = 0.0
    alpha: float = 0.4
    beta: float = 0.35
    gamma: float = 0.25


class ConsciousnessIndex:
    """
    Composite Consciousness Index (C-index) calculator.

    Combines three theoretical perspectives:
    - Integrated Information Theory (Φ)
    - Global Workspace Theory (W-activation)
    - Adaptive Metacognition (A-complexity)
    """

    def __init__(self, alpha: float = 0.4, beta: float = 0.35, gamma: float = 0.25):
        """
        Args:
            alpha: Weight for Φ component
            beta: Weight for W-activation component
            gamma: Weight for A-complexity component

        Note: alpha + beta + gamma should equal 1.0
        """
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

        self.history = []
        self.component_history = []

        logger.info(f"ConsciousnessIndex initialized: α={alpha}, β={beta}, γ={gamma}")

    def calculate(self, phi: float, w_activation: float, a_complexity: float) -> float:
        """
        Calculate C-index from components.

        Args:
            phi: Integrated information value
            w_activation: Workspace activation value
            a_complexity: Adaptive complexity value

        Returns:
            C-index value
        """
        c_index = (
            self.alpha * self._normalize_phi(phi) +
            self.beta * w_activation +
            self.gamma * a_complexity
        )

        c_index = np.clip(c_index, 0.0, 1.0)

        self.history.append(c_index)
        self.component_history.append({
            "phi": phi,
            "w_activation": w_activation,
            "a_complexity": a_complexity
        })

        return float(c_index)

    def _normalize_phi(self, phi: float) -> float:
        """Normalize phi to 0-1 range using sigmoid scaling."""
        return 1.0 / (1.0 + np.exp(-0.5 * (phi - 1.0)))

    def calculate_from_components(self, components: CIndexComponents) -> float:
        """Calculate C-index from CIndexComponents dataclass."""
        return self.calculate(components.phi, components.w_activation, components.a_complexity)

    def get_c_index_stats(self) -> Dict[str, Any]:
        """Get statistics from C-index history."""
        if not self.history:
            return {"count": 0, "mean": 0.0, "max": 0.0, "min": 0.0}

        return {
            "count": len(self.history),
            "mean": float(np.mean(self.history)),
            "max": float(np.max(self.history)),
            "min": float(np.min(self.history)),
            "std": float(np.std(self.history)),
            "last": float(self.history[-1])
        }

    def get_component_contribution(self, component: str) -> float:
        """Get contribution of specific component to overall C-index."""
        weights = {"phi": self.alpha, "w_activation": self.beta, "a_complexity": self.gamma}
        return weights.get(component, 0.0)

    def update_weights(self, alpha: float, beta: float, gamma: float):
        """Update component weights."""
        total = alpha + beta + gamma
        if abs(total - 1.0) > 0.001:
            logger.warning(f"Weights sum to {total}, normalizing to 1.0")
            alpha, beta, gamma = alpha/total, beta/total, gamma/total

        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

        logger.info(f"Weights updated: α={alpha}, β={beta}, γ={gamma}")

    def analyze_trend(self, window: int = 10) -> Dict[str, Any]:
        """Analyze C-index trend over recent history."""
        if len(self.history) < window:
            window = len(self.history)

        if window == 0:
            return {"trend": "unknown", "direction": 0.0, "stability": 0.0}

        recent = self.history[-window:]

        trend_direction = np.mean(np.diff(recent)) if len(recent) > 1 else 0.0

        stability = 1.0 - np.std(recent) if len(recent) > 1 else 1.0

        if trend_direction > 0.05:
            trend = "increasing"
        elif trend_direction < -0.05:
            trend = "decreasing"
        else:
            trend = "stable"

        return {
            "trend": trend,
            "direction": float(trend_direction),
            "stability": float(stability),
            "window": window
        }

    def reset(self):
        """Reset history."""
        self.history = []
        self.component_history = []


class CIndexCalculator:
    """Factory class for creating configured C-index calculators."""

    @staticmethod
    def create_balanced() -> ConsciousnessIndex:
        """Create balanced C-index calculator."""
        return ConsciousnessIndex(alpha=0.4, beta=0.35, gamma=0.25)

    @staticmethod
    def create_phi_focused() -> ConsciousnessIndex:
        """Create Φ-focused calculator."""
        return ConsciousnessIndex(alpha=0.5, beta=0.3, gamma=0.2)

    @staticmethod
    def create_workspace_focused() -> ConsciousnessIndex:
        """Create workspace-focused calculator."""
        return ConsciousnessIndex(alpha=0.3, beta=0.45, gamma=0.25)

    @staticmethod
    def create_metacognition_focused() -> ConsciousnessIndex:
        """Create metacognition-focused calculator."""
        return ConsciousnessIndex(alpha=0.3, beta=0.25, gamma=0.45)

    @staticmethod
    def create_speace_aligned() -> ConsciousnessIndex:
        """Create SPEACE-aligned calculator with DigitalDNA fitness weights."""
        return ConsciousnessIndex(
            alpha=0.35,  # IIT - Information integration
            beta=0.35,   # GWT - Global workspace
            gamma=0.30   # Metacognition - Self-regulation
        )


def calculate_speace_c_index(phi_value: float, w_activation: float, a_complexity: float) -> Tuple[float, Dict[str, float]]:
    """
    Calculate SPEACE-specific C-index with component breakdown.

    Returns:
        Tuple of (c_index, component_contributions)
    """
    c_index_calc = CIndexCalculator.create_speace_aligned()

    c_index = c_index_calc.calculate(phi_value, w_activation, a_complexity)

    contributions = {
        "phi_contribution": c_index_calc.alpha * c_index_calc._normalize_phi(phi_value),
        "w_activation_contribution": c_index_calc.beta * w_activation,
        "a_complexity_contribution": c_index_calc.gamma * a_complexity
    }

    return c_index, contributions


if __name__ == "__main__":
    c_idx = CIndexCalculator.create_speace_aligned()

    test_phi = 0.75
    test_w_activation = 0.6
    test_a_complexity = 0.4

    c_index = c_idx.calculate(test_phi, test_w_activation, test_a_complexity)

    print(f"C-index: {c_index:.4f}")
    print(f"Stats: {c_idx.get_c_index_stats()}")
    print(f"Trend: {c_idx.analyze_trend()}")