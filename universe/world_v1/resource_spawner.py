import random


class ResourceSpawner:
    """
    Spawns resource bundles based on biome classification.
    """

    def __init__(self):
        self.spawn_map = []

    def spawn(self, biome: str):
        if biome == "forest":
            return {"food": random.randint(1, 3)}
        if biome == "grassland":
            return {"food": 1, "material": 1}
        if biome == "desert":
            return {"energy": 1}
        if biome == "tundra":
            return {"material": 1}
        if biome == "rainforest":
            return {"food": 3, "coherence_crystals": 1}
        return {}
