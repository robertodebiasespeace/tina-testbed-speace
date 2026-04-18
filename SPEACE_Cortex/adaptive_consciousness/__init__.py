"""
SPEACE Adaptive Consciousness Framework
Implementation based on IIT, GWT, and Adaptive Metacognition theories

Version: 1.0
Date: 2026-04-18
Integration: SPEACE Cortex v1.0+
"""

from .phi_calculator import PhiCalculator, calculate_fast_phi, calculate_medium_phi, calculate_full_phi
from .workspace import GlobalWorkspace, WorkspaceMetrics
from .metacognitive import MetacognitiveModule, AdaptiveComplexityCalculator
from .consciousness_index import ConsciousnessIndex, CIndexCalculator
from .adaptive_agent import AdaptiveConsciousnessAgent

__all__ = [
    "PhiCalculator",
    "calculate_fast_phi",
    "calculate_medium_phi",
    "calculate_full_phi",
    "GlobalWorkspace",
    "WorkspaceMetrics",
    "MetacognitiveModule",
    "AdaptiveComplexityCalculator",
    "ConsciousnessIndex",
    "CIndexCalculator",
    "AdaptiveConsciousnessAgent",
]

__version__ = "1.0"