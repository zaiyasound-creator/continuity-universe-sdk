import numpy as np


class AetherField:
    """
    Base class for all Aetherion PDE fields.
    Defines API for GPU/CPU update, sampling, and visualization.
    """

    def __init__(self, width: int = 512, height: int = 512):
        self.width = width
        self.height = height
        self.field = np.zeros((height, width), dtype=np.float32)
        self.gpu_buffer = None
        self.name = self.__class__.__name__

    def bind_gpu(self, gpu_buffer):
        self.gpu_buffer = gpu_buffer

    def step_gpu(self, dt: float):
        """Override in GPU solver subclasses."""
        raise NotImplementedError

    def step_cpu(self, dt: float):
        """Override in CPU solver subclasses."""
        raise NotImplementedError

    def step(self, dt: float):
        if self.gpu_buffer is not None:
            self.step_gpu(dt)
        else:
            self.step_cpu(dt)

    def sample(self, x: float, y: float):
        return self.field[int(y) % self.height, int(x) % self.width]
