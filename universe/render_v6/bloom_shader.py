import numpy as np
from scipy.ndimage import gaussian_filter


class AetherBloom:
    """
    Bloom/glow shader for luminous effects.
    """

    def __init__(self, strength: float = 1.6, blur: float = 3.0):
        self.strength = strength
        self.blur = blur

    def apply(self, frame: np.ndarray) -> np.ndarray:
        glow = gaussian_filter(frame.astype(np.float32), sigma=self.blur)
        return np.clip(frame + glow * self.strength, 0, 255).astype(np.uint8)
