from universe.components.base_component import Component


class AABB(Component):
    """Axis-aligned bounding box useful for spatial queries/collision."""

    def __init__(self, x: float = 0.0, y: float = 0.0, w: float = 1.0, h: float = 1.0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
