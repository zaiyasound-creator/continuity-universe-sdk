import numpy as np


class CompositeCPU:
    """
    CPU compositor.
    """

    def __init__(self, alpha: float = 0.5):
        self.alpha = alpha

    def composite(self, base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
        return (base * self.alpha + overlay * (1 - self.alpha)).astype(np.uint8)
