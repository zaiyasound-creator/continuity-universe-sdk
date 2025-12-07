import numpy as np
from scipy.ndimage import gaussian_filter


class CurvatureThunder:
    """
    Radial shockwave bloom from curvature spikes.
    """

    def __init__(self, strength: float = 90, blur: float = 6.0):
        self.strength = strength
        self.blur = blur

    def apply(self, kappa: np.ndarray) -> np.ndarray:
        shock = np.maximum(0, kappa - kappa.mean())
        blurred = gaussian_filter(shock, self.blur)
        img = np.clip(blurred * self.strength, 0, 255).astype(np.uint8)
        return np.stack([img] * 3, axis=-1)
