class Steering:
    """Steering parameters for agents (seek/flee/arrive targets)."""

    def __init__(self, target=None, max_force: float = 1.0):
        self.target = target
        self.max_force = max_force
