class ForceField:
    """
    Base class for fields that generate vector forces on entities.
    """

    def __init__(self):
        self.universe = None

    def bind_universe(self, universe):
        self.universe = universe

    def compute_force(self, position):
        """Override: return a force vector for a position."""
        return 0.0

    def step(self, dt):
        pass  # stateless by default
