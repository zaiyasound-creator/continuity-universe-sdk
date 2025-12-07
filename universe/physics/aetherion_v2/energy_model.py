import numpy as np


class AetherEnergyModel:
    """
    Implements Continuity Physics:
    - κ̇ law
    - Ache/σ feedback
    - entropy gradient ΔS
    - witness-load γ_you injection
    """

    def __init__(self, alpha: float = 0.3, beta: float = 0.2, I_scar: float = 1.0):
        self.alpha = alpha
        self.beta = beta
        self.I_scar = I_scar

    def entropy(self, field: np.ndarray) -> np.ndarray:
        """
        ΔS ≈ local variance (entropy proxy) via 4-neighbor Laplacian magnitude.
        """
        lap = (
            np.roll(field, 1, axis=0)
            + np.roll(field, -1, axis=0)
            + np.roll(field, 1, axis=1)
            + np.roll(field, -1, axis=1)
            - 4 * field
        )
        return np.abs(lap)

    def kappa_dot(self, gamma_you: np.ndarray, deltaS: np.ndarray) -> np.ndarray:
        """
        κ̇ = α γ_you I_scar - β ΔS
        """
        return self.alpha * gamma_you * self.I_scar - self.beta * deltaS
