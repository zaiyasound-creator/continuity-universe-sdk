class VectorField:
    """
    A vector field that returns a 2D/3D vector to apply to objects.
    """

    def __init__(self, fn=lambda pos: (0,0,0)):
        self.fn = fn
        self.universe = None

    def bind_universe(self, universe):
        self.universe = universe

    def sample(self, pos):
        return self.fn(pos)
