class LongTermMemory:
    """
    Episodic/spatial memory storing recent field samples and positions.
    """

    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.events = []

    def record(self, x: float, y: float, sigma: float, ache: float):
        self.events.append((x, y, sigma, ache))
        if len(self.events) > self.capacity:
            self.events.pop(0)

    def preferred_locations(self):
        good = [(e[0], e[1], e[2] - e[3]) for e in self.events]
        if not good:
            return None
        sorted_places = sorted(good, key=lambda t: t[2], reverse=True)
        return sorted_places[:3]
