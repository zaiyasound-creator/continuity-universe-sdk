class EntropyFlowPattern:
    """
    Tracks disorder (entropy) in the universe by sampling field velocities.
    """

    def __init__(self):
        self.entropy = 0.0
        self.universe = None

    def bind_universe(self, universe):
        self.universe = universe

    def evaluate(self, engine, dt):
        total = 0
        for field in engine.fields.values():
            vel = getattr(field, "velocity", 0.0)
            total += abs(vel)

        self.entropy += total * 0.0001 * dt
