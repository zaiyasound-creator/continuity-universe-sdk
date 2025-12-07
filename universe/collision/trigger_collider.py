class TriggerCollider:
    """Trigger volume that detects entry/exit events."""

    def __init__(self, w: float, h: float):
        self.w = w
        self.h = h
        self.active = True
