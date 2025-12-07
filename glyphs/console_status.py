class ConsoleStatusGlyph:
    def __init__(self, every_n_steps=1):
        self.every_n_steps = every_n_steps
        self.counter = 0
        self.universe = None

    def bind_universe(self, universe):
        self.universe = universe

    def render(self, engine):
        self.counter += 1
        # No print to avoid test noise
