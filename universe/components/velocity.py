from universe.components.base_component import Component


class Velocity(Component):
    """Velocity vector for movement systems."""

    def __init__(self, vx: float = 0.0, vy: float = 0.0, vz: float = 0.0):
        self.vx = vx
        self.vy = vy
        self.vz = vz
