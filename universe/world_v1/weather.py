import random


class Weather:
    """
    Generates dynamic storm cells that move across the world, plus coherence blooms.
    """

    def __init__(self, width: int = 200, height: int = 200):
        self.width = width
        self.height = height
        self.storms = []
        self.coherence_blooms = []

    def update(self):
        if random.random() < 0.02:
            self.storms.append(
                {
                    "x": random.randint(0, self.width - 1),
                    "y": random.randint(0, self.height - 1),
                    "strength": random.uniform(0.5, 1.5),
                }
            )

        for s in self.storms:
            s["x"] += random.randint(-2, 2)
            s["y"] += random.randint(-2, 2)

        self.storms = [s for s in self.storms if 0 <= s["x"] < self.width and 0 <= s["y"] < self.height]

        if random.random() < 0.01:
            self.coherence_blooms.append(
                {
                    "x": random.randint(0, self.width - 1),
                    "y": random.randint(0, self.height - 1),
                    "radius": random.randint(5, 15),
                }
            )
