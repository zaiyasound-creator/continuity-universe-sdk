from universe.components.base_component import Component


class Position(Component):
    """2D/3D position component."""

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z
