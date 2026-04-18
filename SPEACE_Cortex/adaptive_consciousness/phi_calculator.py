"""
Phi (Φ) Calculator - Integrated Information Theory Implementation

Implements three levels of Φ approximation:
- Fast-Φ: Lightweight differential entropy based
- Medium-Φ: Network connectivity graph analysis
- Full-Φ: Minimum Information Partition (MIP)

Version: 1.0
Date: 2026-04-18
"""

import numpy as np
from typing import Dict, Any, Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PhiCalculator")


def calculate_fast_phi(state_matrix: np.ndarray) -> float:
    """
    Fast Φ approximation based on differential entropy.

    Args:
        state_matrix: State representation matrix (n x m)

    Returns:
        Φ value (float)
    """
    if state_matrix.size == 0:
        return 0.0

    total_entropy = differential_entropy(state_matrix)

    rows = state_matrix.shape[0]
    if rows < 2:
        return 0.0

    mid = rows // 2
    partition1 = state_matrix[:mid]
    partition2 = state_matrix[mid:]

    partition_entropies = [
        differential_entropy(partition1),
        differential_entropy(partition2)
    ]

    phi = total_entropy - sum(partition_entropies)
    return max(0.0, phi)


def differential_entropy(data: np.ndarray) -> float:
    """
    Calculate differential entropy of data using histogram-based estimation.
    """
    flat = data.flatten()
    if len(flat) < 2:
        return 0.0

    hist, _ = np.histogram(flat, bins='auto', density=True)
    hist = hist[hist > 0]
    if len(hist) == 0:
        return 0.0

    entropy = -np.sum(hist * np.log(hist + 1e-10))
    return entropy


def calculate_medium_phi(connectivity_matrix: np.ndarray) -> float:
    """
    Medium Φ approximation based on network connectivity analysis.

    Args:
        connectivity_matrix: N x N connectivity matrix

    Returns:
        Φ value based on centrality and clustering
    """
    try:
        import networkx as nx

        if connectivity_matrix.shape[0] < 2:
            return 0.0

        G = nx.from_numpy_array(connectivity_matrix)

        centrality = nx.eigenvector_centrality(G, max_iter=1000)
        clustering = nx.clustering(G)

        mean_centrality = np.mean(list(centrality.values())) if centrality else 0.0
        mean_clustering = np.mean(list(clustering.values())) if clustering else 0.0

        phi = mean_centrality * mean_clustering * np.log(connectivity_matrix.shape[0] + 1)

        return float(phi)
    except Exception as e:
        logger.warning(f"Medium phi calculation failed: {e}")
        return 0.0


def calculate_full_phi(state_tensor: np.ndarray, connectivity_tensor: np.ndarray) -> float:
    """
    Full Φ calculation using Minimum Information Partition (MIP).

    This is computationally expensive - use for offline analysis only.

    Args:
        state_tensor: State representation
        connectivity_tensor: Connectivity between elements

    Returns:
        Φ value (float)
    """
    n_elements = state_tensor.shape[0] if len(state_tensor.shape) > 0 else 0

    if n_elements < 2 or n_elements > 10:
        logger.warning(f"Full phi only supports 2-10 elements, got {n_elements}")
        return 0.0

    min_phi = float('inf')

    partitions = generate_bipartitions(n_elements)

    for partition in partitions:
        effective_info = calculate_effective_information(
            state_tensor, connectivity_tensor, partition
        )
        if effective_info < min_phi:
            min_phi = effective_info

    return max(0.0, min_phi)


def generate_bipartitions(n: int) -> list:
    """Generate all possible bipartitions of n elements."""
    from itertools import combinations
    partitions = []

    for r in range(1, n // 2 + 1):
        for combo in combinations(range(n), r):
            mask = np.zeros(n, dtype=bool)
            mask[list(combo)] = True
            partitions.append(mask)

    return partitions


def calculate_effective_information(state_tensor: np.ndarray,
                                    connectivity: np.ndarray,
                                    partition_mask: np.ndarray) -> float:
    """
    Calculate effective information for a given partition.
    """
    true_partition = np.array(partition_mask)

    part_a = state_tensor[true_partition]
    part_b = state_tensor[~true_partition]

    if part_a.size == 0 or part_b.size == 0:
        return 0.0

    mi = mutual_information(part_a, part_b)

    connectivity_a = connectivity[np.ix_(true_partition, true_partition)] if true_partition.sum() > 1 else np.array([[0]])
    connectivity_b = connectivity[np.ix_(~true_partition, ~true_partition)] if (~true_partition).sum() > 1 else np.array([[0]])

    integration_a = np.trace(connectivity_a) / max(1, len(connectivity_a))
    integration_b = np.trace(connectivity_b) / max(1, len(connectivity_b))

    ei = mi * (integration_a + integration_b)

    return ei


def mutual_information(x: np.ndarray, y: np.ndarray) -> float:
    """Calculate mutual information between x and y."""
    try:
        from sklearn.feature_selection import mutual_info_regression
        x_flat = x.flatten().reshape(-1, 1)
        y_flat = y.flatten()

        if len(np.unique(y_flat)) < 2:
            return 0.0

        mi = mutual_info_regression(x_flat, y_flat, random_state=42)[0]
        return float(mi)
    except:
        return 0.0


class PhiCalculator:
    """
    Main Phi calculator class with all three approximation levels.
    """

    def __init__(self, mode: str = "fast"):
        """
        Args:
            mode: "fast", "medium", or "full"
        """
        self.mode = mode
        self.calculation_history = []
        logger.info(f"PhiCalculator initialized in {mode} mode")

    def calculate(self, state_matrix: np.ndarray,
                  connectivity: Optional[np.ndarray] = None) -> float:
        """
        Calculate Phi based on configured mode.
        """
        if self.mode == "fast":
            phi = calculate_fast_phi(state_matrix)
        elif self.mode == "medium":
            if connectivity is None:
                logger.warning("Medium mode requires connectivity matrix, falling back to fast")
                phi = calculate_fast_phi(state_matrix)
            else:
                phi = calculate_medium_phi(connectivity)
        elif self.mode == "full":
            if connectivity is None:
                logger.warning("Full mode requires connectivity tensor, falling back to medium")
                phi = calculate_medium_phi(state_matrix) if len(state_matrix.shape) == 2 else 0.0
            else:
                phi = calculate_full_phi(state_matrix, connectivity)
        else:
            phi = calculate_fast_phi(state_matrix)

        self.calculation_history.append({
            "mode": self.mode,
            "phi_value": phi,
            "timestamp": np.datetime64('now')
        })

        return phi

    def get_phi_stats(self) -> Dict[str, Any]:
        """Get statistics from calculation history."""
        if not self.calculation_history:
            return {"count": 0, "mean": 0.0, "max": 0.0}

        values = [h["phi_value"] for h in self.calculation_history]
        return {
            "count": len(values),
            "mean": np.mean(values),
            "max": np.max(values),
            "min": np.min(values),
            "std": np.std(values)
        }

    def reset_history(self):
        """Reset calculation history."""
        self.calculation_history = []


if __name__ == "__main__":
    test_state = np.random.rand(10, 10)

    calc = PhiCalculator(mode="fast")
    phi_fast = calc.calculate(test_state)
    print(f"Fast Φ: {phi_fast:.4f}")

    calc_medium = PhiCalculator(mode="medium")
    connectivity = np.random.rand(10, 10)
    phi_medium = calc_medium.calculate(test_state, connectivity)
    print(f"Medium Φ: {phi_medium:.4f}")

    print(f"\nPhi Stats: {calc.get_phi_stats()}")