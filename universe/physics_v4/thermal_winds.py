import numpy as np


class ThermalWinds:
    """
    Compute wind vectors from sigma gradients.
    """

    def __init__(self, scale: float = 0.12):
        self.scale = scale

    def compute(self, sigma: np.ndarray):
        gy, gx = np.gradient(sigma)
        vx = gx * self.scale
        vy = gy * self.scale
        return vx, vy
