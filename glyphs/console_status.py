class ConsoleStatusGlyph:
    """
    Placeholder glyph hook that could render status; here it only tracks invocations.
    """

    def __init__(self, every_n_steps: int = 1):
        self.every_n_steps = max(1, int(every_n_steps))
        self.invocations = 0

    def render(self, engine) -> None:
        self.invocations += 1
        # Suppress console output to keep test noise low.
