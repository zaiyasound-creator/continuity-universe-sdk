import numpy as np


class StormMotionBlur:
    """
    Temporal accumulation for storm/agent motion blur.
    """

    def __init__(self, decay: float = 0.88):
        self.decay = decay
        self.buffer = None

    def apply(self, frame: np.ndarray) -> np.ndarray:
        if self.buffer is None:
            self.buffer = frame.astype(np.float32)
        self.buffer = self.buffer * self.decay + frame.astype(np.float32) * (1 - self.decay)
        return np.clip(self.buffer, 0, 255).astype(np.uint8)
