import math

class ScalarField:
    """
    A 1D scalar field defined over universe time or simple coordinates.
    """

    def __init__(self, fn=lambda t: 0):
        self.fn = fn
        self.universe = None

    def bind_universe(self, universe):
        self.universe = universe

    def sample(self, x):
        return self.fn(x)
