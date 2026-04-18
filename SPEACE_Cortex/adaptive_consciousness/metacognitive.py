"""
Metacognitive Module - Adaptive Metacognition Implementation

Implements self-monitoring and regulation of cognitive processes:
- Self-monitoring mechanisms
- Adaptive resource allocation
- Strategy selection based on feedback
- A-complexity calculation

Version: 1.0
Date: 2026-04-18
"""

import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MetacognitiveModule")


@dataclass
class SelfMonitoringData:
    """Data from self-monitoring process."""
    performance_history: List[float] = field(default_factory=list)
    resource_usage: Dict[str, float] = field(default_factory=dict)
    strategy_effectiveness: Dict[str, float] = field(default_factory=dict)
    confidence_level: float = 1.0
    adaptation_needed: bool = False


class MetacognitiveModule:
    """
    Metacognitive module for self-monitoring and regulation.

    Features:
    - Self-monitoring of cognitive processes
    - Adaptive resource allocation
    - Strategy selection based on performance
    - A-complexity calculation
    """

    def __init__(self, hidden_dim: int = 128, monitoring_window: int = 50):
        """
        Args:
            hidden_dim: Dimension of cognitive representations
            monitoring_window: Window size for performance tracking
        """
        self.hidden_dim = hidden_dim
        self.monitoring_window = monitoring_window

        self.performance_history = []
        self.resource_history = []
        self.strategy_history = []

        self.current_strategy = "exploration"
        self.strategies = ["exploration", "exploitation", "recovery", "generalization"]

        self.confidence_threshold = 0.7
        self.adaptation_rate = 0.1

        self.monitoring_data = SelfMonitoringData()

        logger.info(f"MetacognitiveModule initialized: hidden_dim={hidden_dim}")

    def monitor(self, current_state: np.ndarray, action_result: Dict[str, Any]) -> SelfMonitoringData:
        """
        Monitor current cognitive state and update self-model.

        Args:
            current_state: Current cognitive representation
            action_result: Result of last action (reward, success, etc.)

        Returns:
            SelfMonitoringData with current monitoring state
        """
        performance = action_result.get("reward", 0.0) * action_result.get("success", 1.0)

        self.performance_history.append(performance)
        if len(self.performance_history) > self.monitoring_window:
            self.performance_history.pop(0)

        self._update_resource_usage(action_result)

        self._evaluate_strategy_effectiveness()

        self._update_confidence()

        adaptation_needed = self._check_adaptation_need()

        self.monitoring_data = SelfMonitoringData(
            performance_history=self.performance_history.copy(),
            resource_usage=self.monitoring_data.resource_usage.copy(),
            strategy_effectiveness=self.monitoring_data.strategy_effectiveness.copy(),
            confidence_level=self.monitoring_data.confidence_level,
            adaptation_needed=adaptation_needed
        )

        return self.monitoring_data

    def _update_resource_usage(self, action_result: Dict[str, Any]):
        """Track resource usage."""
        resources = {
            "computation": action_result.get("computation_cost", 0.0),
            "memory": action_result.get("memory_usage", 0.0),
            "time": action_result.get("time_cost", 0.0)
        }

        for key, value in resources.items():
            if key not in self.monitoring_data.resource_usage:
                self.monitoring_data.resource_usage[key] = []

            self.monitoring_data.resource_usage[key].append(value)
            if len(self.monitoring_data.resource_usage[key]) > self.monitoring_window:
                self.monitoring_data.resource_usage[key].pop(0)

    def _evaluate_strategy_effectiveness(self):
        """Evaluate how well current strategy is performing."""
        if len(self.performance_history) < 5:
            return

        recent_performance = np.mean(self.performance_history[-5:])

        if self.current_strategy not in self.monitoring_data.strategy_effectiveness:
            self.monitoring_data.strategy_effectiveness[self.current_strategy] = []

        self.monitoring_data.strategy_effectiveness[self.current_strategy].append(recent_performance)

        if len(self.monitoring_data.strategy_effectiveness[self.current_strategy]) > self.monitoring_window:
            self.monitoring_data.strategy_effectiveness[self.current_strategy].pop(0)

    def _update_confidence(self):
        """Update confidence level based on performance variance."""
        if len(self.performance_history) < 3:
            self.monitoring_data.confidence_level = 1.0
            return

        recent = self.performance_history[-10:] if len(self.performance_history) > 10 else self.performance_history

        perf_array = np.array(recent)
        variance = np.var(perf_array)
        mean_perf = np.mean(perf_array)

        if mean_perf > 0:
            cv = np.sqrt(variance) / (mean_perf + 1e-8)
            self.monitoring_data.confidence_level = np.exp(-cv)
        else:
            self.monitoring_data.confidence_level = 0.5

    def _check_adaptation_need(self) -> bool:
        """Check if strategy adaptation is needed."""
        if len(self.performance_history) < self.monitoring_window:
            return False

        window = self.performance_history[-self.monitoring_window:]

        declining = all(window[i] >= window[i+1] for i in range(len(window)-1))

        low_confidence = self.monitoring_data.confidence_level < self.confidence_threshold

        return declining or low_confidence

    def select_strategy(self, context: np.ndarray) -> str:
        """
        Select strategy based on current context and monitoring data.

        Args:
            context: Current cognitive context

        Returns:
            Selected strategy name
        """
        if self.monitoring_data.adaptation_needed:
            best_strategy = self._get_best_strategy()
            if best_strategy != self.current_strategy:
                logger.info(f"Switching strategy: {self.current_strategy} -> {best_strategy}")
                self.current_strategy = best_strategy
                self.strategy_history.append(best_strategy)

        return self.current_strategy

    def _get_best_strategy(self) -> str:
        """Get the strategy with highest historical effectiveness."""
        strategy_scores = {}

        for strategy, performances in self.monitoring_data.strategy_effectiveness.items():
            if len(performances) > 0:
                strategy_scores[strategy] = np.mean(performances[-10:])

        if not strategy_scores:
            return "exploration"

        return max(strategy_scores, key=strategy_scores.get)

    def allocate_resources(self, task_difficulty: float) -> Dict[str, float]:
        """
        Adaptively allocate cognitive resources based on task demands.

        Args:
            task_difficulty: Estimated difficulty of current task (0-1)

        Returns:
            Resource allocation dict
        """
        base_allocation = {
            "attention": 1.0,
            "memory": 1.0,
            "computation": 1.0
        }

        if task_difficulty > 0.7:
            base_allocation["attention"] = 1.5
            base_allocation["computation"] = 1.3
        elif task_difficulty < 0.3:
            base_allocation["memory"] = 0.7
            base_allocation["computation"] = 0.8

        adaptation_factor = 1.0 + self.adaptation_rate * (1.0 - self.monitoring_data.confidence_level)

        for key in base_allocation:
            base_allocation[key] *= adaptation_factor

        return base_allocation

    def get_a_complexity(self) -> float:
        """
        Calculate A-complexity (adaptive complexity) metric.

        Returns:
            A-complexity value
        """
        if len(self.performance_history) < 2:
            return 0.0

        perf_array = np.array(self.performance_history)

        variance = np.var(perf_array)
        mean_perf = np.mean(perf_array)

        adaptation_rate_estimate = np.mean(np.abs(np.diff(perf_array))) if len(perf_array) > 1 else 0.0

        strategy_diversity = len(self.monitoring_data.strategy_effectiveness)

        a_complexity = (
            variance * 0.4 +
            adaptation_rate_estimate * 0.3 +
            strategy_diversity * 0.1 +
            (1.0 - self.monitoring_data.confidence_level) * 0.2
        )

        return float(a_complexity)

    def reset(self):
        """Reset module state."""
        self.performance_history = []
        self.resource_history = []
        self.strategy_history = []
        self.current_strategy = "exploration"
        self.monitoring_data = SelfMonitoringData()
        logger.info("MetacognitiveModule reset")


class AdaptiveComplexityCalculator:
    """Calculator for adaptive complexity metric."""

    def __init__(self):
        self.history = []

    def calculate(self, monitoring_data: SelfMonitoringData) -> float:
        """Calculate A-complexity from monitoring data."""
        if not monitoring_data.performance_history or len(monitoring_data.performance_history) < 2:
            return 0.0

        perf_array = np.array(monitoring_data.performance_history)

        variance = np.var(perf_array) if len(perf_array) > 1 else 0.0

        trend = np.mean(np.diff(perf_array)) if len(perf_array) > 1 else 0.0

        confidence_penalty = 1.0 - monitoring_data.confidence_level

        a_complexity = variance + abs(trend) + confidence_penalty

        self.history.append(a_complexity)

        return float(a_complexity)


if __name__ == "__main__":
    metacog = MetacognitiveModule(hidden_dim=64)

    test_state = np.random.rand(64)

    for i in range(20):
        action_result = {
            "reward": np.random.rand() * (1.0 if i > 5 else 0.5),
            "success": np.random.rand() > 0.3,
            "computation_cost": np.random.rand() * 0.5,
            "memory_usage": np.random.rand() * 0.3,
            "time_cost": np.random.rand() * 0.2
        }

        monitoring = metacog.monitor(test_state, action_result)

    strategy = metacog.select_strategy(test_state)
    resources = metacog.allocate_resources(0.6)
    a_complexity = metacog.get_a_complexity()

    print(f"Current strategy: {strategy}")
    print(f"Resource allocation: {resources}")
    print(f"A-complexity: {a_complexity:.4f}")
    print(f"Confidence: {monitoring.confidence_level:.4f}")