import numpy as np


class AetherStorms:
    """
    Random disturbance injectors producing spikes/bursts.
    """

    def __init__(self, intensity: float = 3.0, frequency: float = 0.003):
        self.intensity = intensity
        self.frequency = frequency

    def apply(self, sigma: np.ndarray, ache: np.ndarray, kappa: np.ndarray):
        if np.random.random() < self.frequency:
            h, w = sigma.shape
            cx = np.random.randint(0, w)
            cy = np.random.randint(0, h)

            sigma[cy, cx] += self.intensity
            ache[cy, cx] += self.intensity * 0.6
            kappa[cy, cx] += self.intensity * 0.3
