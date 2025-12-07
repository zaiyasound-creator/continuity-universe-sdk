import numpy as np


class TurbulenceDriver:
    """
    Noise-based turbulence driver for flowfields.
    """

    def __init__(self, strength: float = 0.02):
        self.strength = strength

    def apply(self, phi_x: np.ndarray, phi_y: np.ndarray):
        noise = (np.random.random(phi_x.shape) - 0.5) * self.strength
        phi_x += noise
        phi_y += noise
