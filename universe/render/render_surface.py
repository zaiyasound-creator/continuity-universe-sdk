import numpy as np


class RenderSurface:
    """
    Stores the final rendered frame buffer.
    """

    def __init__(self, width: int, height: int):
        self.w = width
        self.h = height
        self.buffer = np.zeros((height, width, 3), np.uint8)

    def blit(self, img: np.ndarray):
        self.buffer = img

    def get_frame(self):
        return self.buffer
