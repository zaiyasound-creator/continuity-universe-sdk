import numpy as np


class TurbulenceCPU:
    """Simple stable fluid-like solver using vorticity influence."""

    def __init__(self, viscosity: float = 0.001):
        self.viscosity = viscosity

    @staticmethod
    def vorticity(vx, vy):
        return (
            np.roll(vy, -1, axis=1)
            - np.roll(vy, 1, axis=1)
            - np.roll(vx, -1, axis=0)
            + np.roll(vx, 1, axis=0)
        )

    def step(self, vx, vy, dt: float):
        vort = self.vorticity(vx, vy)
        vx = vx + self.viscosity * vort * dt
        vy = vy - self.viscosity * vort * dt
        return vx, vy
