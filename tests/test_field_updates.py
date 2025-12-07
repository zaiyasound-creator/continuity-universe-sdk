class DummyField:
    def __init__(self):
        self.updated = False
    def step(self, dt):
        self.updated = True

def test_field_update_called():
    from universe.engine.universe_engine import UniverseEngine
    U = UniverseEngine()

    field = DummyField()
    U.register_field("dummy", field)

    U.step(1.0)
    assert field.updated is True
