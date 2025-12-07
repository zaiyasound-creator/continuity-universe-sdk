import numpy as np


class StormGlow:
    """
    Glow effect from sigma surges and Ache spikes.
    """

    def __init__(self, intensity: float = 120):
        self.intensity = intensity

    def apply(self, sigma: np.ndarray, ache: np.ndarray) -> np.ndarray:
        surge = np.maximum(sigma * 0.6, ache * 0.4)
        glow = np.clip(surge * self.intensity, 0, 255).astype(np.uint8)
        return np.stack([glow, glow, glow], axis=-1)
