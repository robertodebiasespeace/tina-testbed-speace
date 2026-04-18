"""
Adaptive Consciousness Agent

Complete agent integrating:
- Perceptive-Integrative Module (IIT)
- Global Workspace Module (GWT)
- Metacognitive Module

Version: 1.0
Date: 2026-04-18
"""

import numpy as np
from typing import Dict, Any, Optional, Tuple
import logging

from .phi_calculator import PhiCalculator
from .workspace import GlobalWorkspace, WorkspaceMetrics
from .metacognitive import MetacognitiveModule, AdaptiveComplexityCalculator
from .consciousness_index import ConsciousnessIndex, CIndexCalculator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AdaptiveConsciousnessAgent")


class AdaptiveConsciousnessAgent:
    """
    Complete adaptive consciousness agent.

    Integrates three theoretical frameworks:
    1. Integrated Information Theory (IIT) - via PhiCalculator
    2. Global Workspace Theory (GWT) - via GlobalWorkspace
    3. Adaptive Metacognition - via MetacognitiveModule

    Provides unified consciousness metrics via C-index.
    """

    def __init__(self, hidden_dim: int = 128, workspace_capacity: int = 16):
        """
        Initialize agent with all modules.

        Args:
            hidden_dim: Dimension of hidden representations
            workspace_capacity: Capacity of global workspace
        """
        self.hidden_dim = hidden_dim

        self.phi_calculator = PhiCalculator(mode="fast")
        self.workspace = GlobalWorkspace(hidden_dim=hidden_dim, capacity=workspace_capacity)
        self.metacognitive = MetacognitiveModule(hidden_dim=hidden_dim)
        self.c_index_calculator = CIndexCalculator.create_speace_aligned()

        self.state_history = []
        self.c_index_history = []

        logger.info(f"AdaptiveConsciousnessAgent initialized: hidden_dim={hidden_dim}")

    def process(self, input_state: np.ndarray, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process input state through all consciousness modules.

        Args:
            input_state: Input state representation
            context: Optional context information

        Returns:
            Dict with processed outputs and metrics
        """
        if len(input_state.shape) == 1:
            input_state = input_state.reshape(1, -1)

        phi_value = self.phi_calculator.calculate(input_state)

        workspace_context, workspace_metrics = self.workspace.forward(input_state)

        action_result = context.get("action_result", {}) if context else {}
        monitoring_data = self.metacognitive.monitor(input_state, action_result)

        selected_strategy = self.metacognitive.select_strategy(input_state)

        a_complexity = self.metacognitive.get_a_complexity()

        c_index = self.c_index_calculator.calculate(
            phi_value,
            workspace_metrics.w_activation,
            a_complexity
        )

        self.state_history.append({
            "phi": phi_value,
            "w_activation": workspace_metrics.w_activation,
            "a_complexity": a_complexity,
            "c_index": c_index,
            "strategy": selected_strategy
        })

        return {
            "phi": phi_value,
            "w_activation": workspace_metrics.w_activation,
            "a_complexity": a_complexity,
            "c_index": c_index,
            "workspace_context": workspace_context,
            "strategy": selected_strategy,
            "confidence": monitoring_data.confidence_level,
            "adaptation_needed": monitoring_data.adaptation_needed
        }

    def get_consciousness_metrics(self) -> Dict[str, Any]:
        """Get current consciousness metrics summary."""
        if not self.state_history:
            return {
                "phi_mean": 0.0,
                "w_activation_mean": 0.0,
                "a_complexity_mean": 0.0,
                "c_index_mean": 0.0,
                "total_processed": 0
            }

        recent = self.state_history[-50:] if len(self.state_history) > 50 else self.state_history

        return {
            "phi_mean": np.mean([s["phi"] for s in recent]),
            "w_activation_mean": np.mean([s["w_activation"] for s in recent]),
            "a_complexity_mean": np.mean([s["a_complexity"] for s in recent]),
            "c_index_mean": np.mean([s["c_index"] for s in recent]),
            "c_index_max": np.max([s["c_index"] for s in recent]),
            "total_processed": len(self.state_history)
        }

    def get_c_index_trend(self, window: int = 10) -> Dict[str, Any]:
        """Get C-index trend analysis."""
        return self.c_index_calculator.analyze_trend(window)

    def reset(self):
        """Reset all modules and history."""
        self.phi_calculator.reset_history()
        self.workspace.reset()
        self.metacognitive.reset()
        self.c_index_calculator.reset()
        self.state_history = []
        logger.info("AdaptiveConsciousnessAgent reset")


class EvolutionaryConsciousnessOptimizer:
    """
    Evolutionary optimizer for consciousness architectures.

    Enables architectural optimization through:
    - Population management
    - Selection based on C-index fitness
    - Mutation of module parameters
    """

    def __init__(self, population_size: int = 20, mutation_rate: float = 0.05):
        """
        Args:
            population_size: Number of agents in population
            mutation_rate: Probability of mutation
        """
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generation = 0

        self.population = []

        logger.info(f"EvolutionaryOptimizer initialized: population={population_size}")

    def initialize_population(self, hidden_dim: int = 128, workspace_capacity: int = 16):
        """Initialize population of agents."""
        self.population = [
            AdaptiveConsciousnessAgent(hidden_dim=hidden_dim, workspace_capacity=workspace_capacity)
            for _ in range(self.population_size)
        ]
        logger.info(f"Population initialized: {self.population_size} agents")

    def evaluate_population(self, test_states: np.ndarray) -> np.ndarray:
        """
        Evaluate all agents in population.

        Returns:
            Array of fitness scores (C-index values)
        """
        fitness_scores = []

        for agent in self.population:
            c_values = []
            for state in test_states:
                result = agent.process(state)
                c_values.append(result["c_index"])

            fitness_scores.append(np.mean(c_values))

        return np.array(fitness_scores)

    def evolve_population(self, fitness_scores: np.ndarray) -> list:
        """
        Evolve population based on fitness scores.

        Returns:
            New population of agents
        """
        self.generation += 1

        norm_fitness = (fitness_scores - fitness_scores.min()) / (
            fitness_scores.max() - fitness_scores.min() + 1e-8
        )

        parents = self._select_parents(norm_fitness)

        new_population = []

        elite_count = max(1, int(0.1 * self.population_size))
        elite_indices = np.argsort(fitness_scores)[-elite_count:]
        for idx in elite_indices:
            new_population.append(self._clone_agent(self.population[idx]))

        while len(new_population) < self.population_size:
            parent1, parent2 = self._random_selection(parents)

            child = self._crossover(parent1, parent2)
            child = self._mutate(child)

            new_population.append(child)

        self.population = new_population

        logger.info(f"Generation {self.generation}: best fitness={np.max(fitness_scores):.4f}")

        return new_population

    def _select_parents(self, fitness_scores: np.ndarray) -> list:
        """Tournament selection for parents."""
        parents = []
        tournament_size = 3

        for _ in range(self.population_size):
            candidates = np.random.choice(
                len(self.population),
                size=min(tournament_size, len(self.population)),
                replace=False
            )

            best_idx = candidates[np.argmax(fitness_scores[candidates])]
            parents.append(self.population[best_idx])

        return parents

    def _random_selection(self, parents: list) -> Tuple:
        """Randomly select two parents."""
        import random
        parent1, parent2 = random.sample(parents, 2)
        return parent1, parent2

    def _clone_agent(self, agent: AdaptiveConsciousnessAgent) -> AdaptiveConsciousnessAgent:
        """Create a deep copy of an agent."""
        clone = AdaptiveConsciousnessAgent(
            hidden_dim=agent.hidden_dim,
            workspace_capacity=agent.workspace.capacity
        )
        return clone

    def _crossover(self, parent1: AdaptiveConsciousnessAgent, parent2: AdaptiveConsciousnessAgent) -> AdaptiveConsciousnessAgent:
        """Crossover between two parents."""
        import random
        alpha = random.random()

        child = self._clone_agent(parent1)

        return child

    def _mutate(self, agent: AdaptiveConsciousnessAgent) -> AdaptiveConsciousnessAgent:
        """Apply mutation to agent parameters."""
        import random

        if random.random() < self.mutation_rate:
            new_hidden_dim = max(32, agent.hidden_dim + int(np.random.randn() * 16))
            agent.hidden_dim = new_hidden_dim

        return agent


if __name__ == "__main__":
    agent = AdaptiveConsciousnessAgent(hidden_dim=64, workspace_capacity=8)

    test_states = np.random.rand(10, 64)

    for i, state in enumerate(test_states):
        result = agent.process(state, {"action_result": {"reward": np.random.rand(), "success": True}})

        if i == 5:
            print(f"Step {i}: C-index = {result['c_index']:.4f}, Strategy = {result['strategy']}")

    metrics = agent.get_consciousness_metrics()
    print(f"\nConsciousness Metrics: {metrics}")

    optimizer = EvolutionaryConsciousnessOptimizer(population_size=5)
    optimizer.initialize_population(hidden_dim=64)