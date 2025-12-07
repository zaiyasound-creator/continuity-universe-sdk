class AsciiBarGlyph:
    def __init__(self, fn, width=30):
        self.fn = fn
        self.width = width
        self.universe = None

    def bind_universe(self, universe):
        self.universe = universe

    def render(self, engine):
        value = self.fn(engine)
        bars = int(value * self.width)
        print("[" + "#"*bars + "-"*(self.width-bars) + "]", value)
