import numpy as np


class GPUBuffers:
    """
    Host-side buffers for staging SoA data before transfer to device.
    """

    def __init__(self, max_entities: int = 50000):
        self.max = max_entities
        self.pos_x = np.zeros(self.max, dtype=np.float32)
        self.pos_y = np.zeros(self.max, dtype=np.float32)
        self.vel_x = np.zeros(self.max, dtype=np.float32)
        self.vel_y = np.zeros(self.max, dtype=np.float32)
        self.radius = np.ones(self.max, dtype=np.float32)
        self.mass = np.ones(self.max, dtype=np.float32)

    def reset(self):
        self.pos_x.fill(0)
        self.pos_y.fill(0)
        self.vel_x.fill(0)
        self.vel_y.fill(0)
        self.radius.fill(1)
        self.mass.fill(1)
