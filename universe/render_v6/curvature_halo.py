import numpy as np


class CurvatureHalo:
    """
    Produces halo intensity from curvature gradients.
    """

    def __init__(self, strength: float = 40.0):
        self.strength = strength

    def apply(self, kappa: np.ndarray) -> np.ndarray:
        gy, gx = np.gradient(kappa)
        mag = np.sqrt(gx * gx + gy * gy)
        halo = np.clip(mag * self.strength, 0, 255).astype(np.uint8)
        return halo
