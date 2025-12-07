import numpy as np


class AetherRain:
    """
    Coherence particles falling with drift; brightness scales with height.
    """

    def __init__(self, count: int = 600):
        self.count = count
        self.x = np.random.rand(count)
        self.y = np.random.rand(count)
        self.v = np.random.rand(count) * 0.004 + 0.003

    def step(self, dt: float, sigma: np.ndarray):
        self.y += self.v * dt
        self.y %= 1.0
        brightness = np.interp(self.y, [0, 1], [80, 255])
        return self.x, self.y, brightness
