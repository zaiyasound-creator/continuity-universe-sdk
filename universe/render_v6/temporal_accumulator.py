import numpy as np


class TemporalAccumulator:
    """
    Temporal accumulation buffer for motion trails/afterglow.
    """

    def __init__(self, width: int, height: int, decay: float = 0.92):
        self.decay = decay
        self.buffer = np.zeros((height, width, 3), np.float32)

    def accumulate(self, frame: np.ndarray) -> np.ndarray:
        self.buffer = self.buffer * self.decay + frame.astype(np.float32) * (1 - self.decay)
        return np.clip(self.buffer, 0, 255).astype(np.uint8)
