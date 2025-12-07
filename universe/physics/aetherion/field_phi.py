import numpy as np

from universe.physics.aetherion.field_base import AetherField


class PhiField(AetherField):
    """
    Vector field controlling drift and directional flow driven by gradients.
    """

    def __init__(self, width: int = 512, height: int = 512, solver=None):
        super().__init__(width, height)
        self.solver = solver
        self.vx = np.zeros_like(self.field)
        self.vy = np.zeros_like(self.field)

    def step_cpu(self, dt: float):
        # Basic gradient-driven flow on CPU
        self.vx += dt * (np.roll(self.field, -1, axis=1) - np.roll(self.field, 1, axis=1))
        self.vy += dt * (np.roll(self.field, -1, axis=0) - np.roll(self.field, 1, axis=0))

    def step_gpu(self, dt: float):
        # Placeholder GPU path; falls back to CPU behavior
        self.step_cpu(dt)
