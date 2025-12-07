import math


class SeasonCycle:
    """
    Produces a seasonal oscillation in range [-1, 1].
    """

    def __init__(self):
        self.time = 0.0

    def step(self, dt: float = 1.0):
        self.time += dt
        return math.sin(self.time / 300.0)  # long seasonal cycle
