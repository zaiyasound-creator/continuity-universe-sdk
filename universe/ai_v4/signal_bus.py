from universe.ai_v4.signal import Signal


class SignalBus:
    """
    Local communication network for agents.
    """

    def __init__(self):
        self.signals = []

    def emit(self, signal: Signal):
        self.signals.append(signal)

    def nearby(self, x: float, y: float, radius: float = 12.0):
        return [s for s in self.signals if abs(s.x - x) < radius and abs(s.y - y) < radius]

    def clear(self):
        self.signals.clear()
