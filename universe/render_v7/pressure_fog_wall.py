import numpy as np


class PressureFogWall:
    """
    Visualizes Ache pressure fronts as fog walls.
    """

    def __init__(self, scale: float = 1.8):
        self.scale = scale

    def apply(self, ache: np.ndarray) -> np.ndarray:
        gy, gx = np.gradient(ache)
        mag = np.sqrt(gx * gx + gy * gy)
        wall = np.clip(mag * self.scale, 0, 255).astype(np.uint8)
        return np.stack([wall] * 3, axis=-1)
