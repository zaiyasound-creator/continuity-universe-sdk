class DummyPattern:
    def __init__(self):
        self.called = False
    def evaluate(self, engine, dt):
        self.called = True

def test_pattern_evaluation_called():
    from universe.engine.universe_engine import UniverseEngine
    U = UniverseEngine()

    pat = DummyPattern()
    U.register_pattern(pat)

    U.step(1.0)
    assert pat.called is True
