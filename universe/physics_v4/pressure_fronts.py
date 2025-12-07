import numpy as np


class PressureFronts:
    """
    Compute pressure vectors from Ache gradients (entropy pressure).
    """

    def __init__(self, scale: float = 1.5):
        self.scale = scale

    def compute(self, ache: np.ndarray):
        gy, gx = np.gradient(ache)
        px = -gx * self.scale
        py = -gy * self.scale
        return px, py
