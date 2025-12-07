import numpy as np


class FlowDistortion:
    """
    Applies flow-based distortion (shimmer/heat haze).
    """

    def __init__(self, amount: float = 4.0):
        self.amount = amount

    def apply(self, frame: np.ndarray, vx: np.ndarray, vy: np.ndarray) -> np.ndarray:
        h, w, _ = frame.shape
        out = np.zeros_like(frame)

        for y in range(h):
            for x in range(w):
                dx = int(vx[y, x] * self.amount)
                dy = int(vy[y, x] * self.amount)
                out[y, x] = frame[(y + dy) % h, (x + dx) % w]

        return out
