class DummyGlyph:
    def __init__(self):
        self.called = False
    def render(self, engine):
        self.called = True

def test_glyph_render_called():
    from universe.engine.universe_engine import UniverseEngine
    U = UniverseEngine()

    glyph = DummyGlyph()
    U.register_glyph(glyph)

    U.step(1.0)
    assert glyph.called is True
