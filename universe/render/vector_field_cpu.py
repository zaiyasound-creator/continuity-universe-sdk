import numpy as np


class VectorFieldCPU:
    """
    Converts (vx, vy) into an RGB overlay encoding magnitude and direction.
    """

    def __init__(self, scale: float = 20):
        self.scale = scale

    def render(self, vx: np.ndarray, vy: np.ndarray) -> np.ndarray:
        h, w = vx.shape
        img = np.zeros((h, w, 3), np.uint8)

        mag = np.sqrt(vx * vx + vy * vy)
        mmax = mag.max() if mag.max() != 0 else 1.0

        img[..., 0] = (mag / mmax * 255).astype(np.uint8)

        angle = np.arctan2(vy, vx)
        img[..., 1] = ((np.sin(angle) + 1) / 2 * 255).astype(np.uint8)
        img[..., 2] = ((np.cos(angle) + 1) / 2 * 255).astype(np.uint8)

        return img
