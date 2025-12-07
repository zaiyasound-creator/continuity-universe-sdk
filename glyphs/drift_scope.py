class DriftScopeGlyph:
    def __init__(self, monitor):
        self.monitor = monitor

    def render(self, engine):
        print(f"[Drift] {self.monitor.drift:.4f}")
