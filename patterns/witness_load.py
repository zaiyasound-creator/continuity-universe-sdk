class WitnessLoad:
    """
    Increase load as more systems interact per step.
    """

    def __init__(self):
        self.load = 0.0
        self.universe = None

    def bind_universe(self, universe):
        self.universe = universe

    def evaluate(self, engine, dt):
        interactions = len(engine.fields) + len(engine.patterns)
        self.load += interactions * 0.001 * dt
