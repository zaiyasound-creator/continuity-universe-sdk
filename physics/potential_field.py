class PotentialField:
    def __init__(self, potential_fn):
        self.V = potential_fn  # potential function V(x)
        self.universe = None

    def bind_universe(self, universe):
        self.universe = universe

    def force(self, x):
        eps = 1e-4
        # F = - dV/dx
        return -(self.V(x + eps) - self.V(x - eps)) / (2 * eps)
