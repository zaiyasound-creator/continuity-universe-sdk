class TrailRenderer:
    """Stores recent positions for entities to render trails."""

    def __init__(self, length: int = 3, color=(150, 150, 255)):
        self.length = length
        self.history = {}  # eid -> list of positions
        self.color = color

    def add_point(self, eid, x: float, y: float):
        arr = self.history.setdefault(eid, [])
        arr.append((x, y))
        if len(arr) > self.length:
            arr.pop(0)

    def get_trail(self, eid):
        return self.history.get(eid, [])
