class FadeEffects:
    """Fade in/out color modulation."""

    def __init__(self):
        self.active = None  # (mode, total, t)

    def fade_in(self, duration: float):
        self.active = ("in", duration, 0.0)

    def fade_out(self, duration: float):
        self.active = ("out", duration, 0.0)

    def apply(self, char: str, r: int, g: int, b: int, dt: float):
        if not self.active:
            return char, r, g, b

        mode, total, t = self.active
        t += dt
        self.active = (mode, total, t)
        factor = min(t / total, 1.0)

        if mode == "out":
            r = int(r * (1 - factor))
            g = int(g * (1 - factor))
            b = int(b * (1 - factor))
        elif mode == "in":
            r = int(r * factor)
            g = int(g * factor)
            b = int(b * factor)

        if factor >= 1.0:
            self.active = None

        return char, r, g, b
