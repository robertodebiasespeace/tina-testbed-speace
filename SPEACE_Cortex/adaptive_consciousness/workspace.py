"""
Global Workspace Module - Global Workspace Theory Implementation

Implements competitive access to a limited-capacity workspace:
- Content-based competition
- Top-k selection mechanism
- Workspace activation metrics (W-activation)

Version: 1.0
Date: 2026-04-18
"""

import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GlobalWorkspace")


@dataclass
class WorkspaceMetrics:
    """Metrics for global workspace operation."""
    w_activation: float = 0.0
    information_broadcast: float = 0.0
    competition_intensity: float = 0.0
    workspace_coherence: float = 0.0
    timestamp: str = field(default_factory=lambda: str(np.datetime64('now')))


class GlobalWorkspace:
    """
    Global Workspace implementation based on GWT.

    Features:
    - Limited-capacity workspace memory
    - Content-based competition for access
    - Attention mechanism for filtering
    - W-activation metric calculation
    """

    def __init__(self, hidden_dim: int = 128, capacity: int = 16, num_heads: int = 4):
        """
        Args:
            hidden_dim: Dimension of hidden representations
            capacity: Maximum items in workspace
            num_heads: Number of attention heads
        """
        self.hidden_dim = hidden_dim
        self.capacity = capacity
        self.num_heads = num_heads

        self.workspace_memory = np.zeros((capacity, hidden_dim))
        self.attention_weights = np.eye(hidden_dim)

        self.competition_scores_history = []
        self.activation_history = []
        self.access_patterns = []

        self.persistence = 0.8

        logger.info(f"GlobalWorkspace initialized: capacity={capacity}, hidden_dim={hidden_dim}")

    def forward(self, integrated_states: np.ndarray) -> Tuple[np.ndarray, WorkspaceMetrics]:
        """
        Process integrated states through workspace competition.

        Args:
            integrated_states: (batch, seq, hidden) integrated representations

        Returns:
            Tuple of (workspace_context, metrics)
        """
        if len(integrated_states.shape) == 2:
            integrated_states = integrated_states.unsqueeze(0) if hasattr(integrated_states, 'unsqueeze') else np.expand_dims(integrated_states, 0)

        batch_size, seq_len, hidden_dim = integrated_states.shape

        competition_scores = self._compute_competition(integrated_states)

        k = max(1, self.capacity // 2)
        access_mask = self._top_k_selection(competition_scores, k)

        workspace_context, attention_output = self._compute_attention(
            integrated_states, access_mask
        )

        self._update_workspace(integrated_states, access_mask)

        metrics = self._calculate_metrics(
            competition_scores, access_mask, workspace_context
        )

        self.activation_history.append(metrics.w_activation)

        return workspace_context, metrics

    def _compute_competition(self, states: np.ndarray) -> np.ndarray:
        """Compute competition scores based on content."""
        flat_states = states.reshape(-1, self.hidden_dim)

        norms = np.linalg.norm(flat_states, axis=1, keepdims=True)
        normalized = flat_states / (norms + 1e-8)

        relevance = np.sum(normalized * np.mean(self.workspace_memory, axis=0), axis=1)

        competition_scores = self._sigmoid(relevance)

        self.competition_scores_history.append(competition_scores.mean())

        return competition_scores

    def _sigmoid(self, x: np.ndarray) -> np.ndarray:
        """Sigmoid activation."""
        return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))

    def _top_k_selection(self, scores: np.ndarray, k: int) -> np.ndarray:
        """
        Top-k selection for workspace access.

        Returns:
            Boolean mask of selected items
        """
        flat_scores = scores.flatten()

        if len(flat_scores) <= k:
            access_mask = np.ones_like(flat_scores, dtype=bool)
        else:
            threshold = np.sort(flat_scores)[-k]
            access_mask = flat_scores >= threshold

        self.access_patterns.append(access_mask.astype(float))

        return access_mask

    def _compute_attention(self, states: np.ndarray, access_mask: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Compute attention-based workspace output."""
        batch_size, seq_len, hidden_dim = states.shape

        workspace_mean = np.mean(self.workspace_memory, axis=0, keepdims=True)
        workspace_expanded = np.tile(workspace_mean, (batch_size, seq_len, 1))

        attention_scores = np.sum(states * workspace_expanded, axis=2, keepdims=True)
        attention_weights = self._softmax(attention_scores, axis=1)

        attention_output = np.sum(states * attention_weights, axis=1)

        return attention_output, attention_weights.flatten()

    def _softmax(self, x: np.ndarray, axis: int = -1) -> np.ndarray:
        """Softmax activation."""
        exp_x = np.exp(x - np.max(x, axis=axis, keepdims=True))
        return exp_x / (np.sum(exp_x, axis=axis, keepdims=True) + 1e-8)

    def _update_workspace(self, states: np.ndarray, access_mask: np.ndarray):
        """Update workspace memory based on accessed states."""
        batch_size, seq_len, hidden_dim = states.shape

        flat_states = states.reshape(-1, hidden_dim)
        flat_mask = access_mask.flatten()

        if not np.any(flat_mask):
            return

        accessed_states = flat_states[flat_mask]

        if len(accessed_states.shape) == 1:
            accessed_states = accessed_states.reshape(1, -1)

        if accessed_states.shape[0] > 0:
            new_content = np.mean(accessed_states, axis=0)

            new_content_norm = new_content / (np.linalg.norm(new_content) + 1e-8)

            self.workspace_memory = (
                self.persistence * self.workspace_memory +
                (1 - self.persistence) * new_content_norm
            )

    def _calculate_metrics(self, competition_scores: np.ndarray,
                          access_mask: np.ndarray,
                          context: np.ndarray) -> WorkspaceMetrics:
        """Calculate workspace metrics."""
        w_activation = np.mean(access_mask.astype(float))

        info_broadcast = np.std(competition_scores)

        competition_intensity = np.mean(np.abs(competition_scores - 0.5) * 2)

        if len(self.access_patterns) > 1:
            coherence = 1.0 - np.mean([
                np.sum(np.abs(p1 - p2)) / len(p1)
                for p1, p2 in zip(self.access_patterns[-10:-1], self.access_patterns[-9:])
            ])
        else:
            coherence = 1.0

        return WorkspaceMetrics(
            w_activation=w_activation,
            information_broadcast=info_broadcast,
            competition_intensity=competition_intensity,
            workspace_coherence=coherence
        )

    def get_workspace_state(self) -> Dict[str, Any]:
        """Get current workspace state."""
        return {
            "memory_shape": self.workspace_memory.shape,
            "memory_norm": float(np.linalg.norm(self.workspace_memory)),
            "activation_mean": float(np.mean(self.activation_history[-100:])) if self.activation_history else 0.0,
            "access_pattern_diversity": float(np.mean(self.access_patterns[-100:]).std()) if len(self.access_patterns) > 1 else 0.0
        }

    def reset(self):
        """Reset workspace memory and history."""
        self.workspace_memory = np.zeros((self.capacity, self.hidden_dim))
        self.activation_history = []
        self.competition_scores_history = []
        self.access_patterns = []
        logger.info("Workspace reset")


if __name__ == "__main__":
    ws = GlobalWorkspace(hidden_dim=64, capacity=8)

    test_states = np.random.rand(2, 10, 64)

    context, metrics = ws.forward(test_states)

    print(f"W-activation: {metrics.w_activation:.4f}")
    print(f"Information broadcast: {metrics.information_broadcast:.4f}")
    print(f"Competition intensity: {metrics.competition_intensity:.4f}")
    print(f"Workspace coherence: {metrics.workspace_coherence:.4f}")