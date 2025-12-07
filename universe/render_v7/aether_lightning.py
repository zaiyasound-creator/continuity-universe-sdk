import numpy as np


class AetherLightning:
    """
    Lightning strikes based on curvature gradients and random chance.
    """

    def __init__(self, frequency: float = 0.002, strength: int = 255):
        self.frequency = frequency
        self.strength = strength

    def apply(self, kappa: np.ndarray) -> np.ndarray:
        if np.random.random() > self.frequency:
            return np.zeros((*kappa.shape, 3), np.uint8)

        h, w = kappa.shape
        bolt = np.zeros((h, w), np.uint8)

        gy, gx = np.gradient(kappa)
        mag = np.sqrt(gx * gx + gy * gy)
        bolt[mag > mag.mean() * 2.5] = self.strength

        return np.stack([bolt] * 3, axis=-1)
