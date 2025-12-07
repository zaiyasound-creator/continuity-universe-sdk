class AABBCollider:
    """Axis-aligned bounding box collider."""

    def __init__(self, w: float, h: float):
        self.w = w
        self.h = h


class CircleCollider:
    """Circle collider."""

    def __init__(self, r: float):
        self.r = r
