class Glow:
    """Tracks emissive entities for glow coloring."""

    def __init__(self):
        self.emissive_entities = []

    def add(self, eid, color=(255, 180, 80)):
        self.emissive_entities.append((eid, color))

    def sample(self, eid):
        for tid, color in self.emissive_entities:
            if tid == eid:
                return color
        return None
