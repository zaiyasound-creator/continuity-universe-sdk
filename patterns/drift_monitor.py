class DriftMonitor:
    """
    Detects divergence (drift) in engine states.
    """

    def __init__(self):
        self.drift = 0.0
        self.universe = None

    def bind_universe(self, universe):
        self.universe = universe

    def evaluate(self, engine, dt):
        self.drift += len(engine.fields) * 0.00005 * dt
