class ReciprocityBalance:
    """
    Balances drift vs coherence levels.
    """

    def __init__(self, gain=0.1):
        self.value = 1.0
        self.gain = gain
        self.universe = None

    def bind_universe(self, universe):
        self.universe = universe

    def evaluate(self, engine, dt):
        coherence = sum(
            getattr(p, "coherence", 1.0) for p in engine.patterns
        ) / max(1, len(engine.patterns))

        self.value += (coherence - self.value) * self.gain * dt
