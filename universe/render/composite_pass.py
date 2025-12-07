import numpy as np


class CompositePass:
    """
    Composites two images with a blend factor.
    """

    def __init__(self, alpha: float = 0.6):
        self.alpha = alpha

    def composite(self, base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
        return (base * self.alpha + overlay * (1 - self.alpha)).astype(np.uint8)
