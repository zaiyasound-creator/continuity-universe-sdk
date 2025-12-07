import math


class DayNightCycle:
    """
    Planetary day/night simulation returning a light level in [0, 1].
    """

    def __init__(self):
        self.time = 0.0
        self.light_level = 1.0

    def step(self, dt: float = 1.0):
        self.time += dt
        self.light_level = (math.sin(self.time / 300.0) + 1) / 2
        return self.light_level
