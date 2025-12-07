import logging


def test_engine_boot():
    from universe.engine.universe_engine import UniverseEngine

    U = UniverseEngine()
    assert U.time == 0


def test_duplicate_field_registration_raises():
    from universe.engine.universe_engine import UniverseEngine

    class DummyField:
        def step(self, dt):
            return dt

    U = UniverseEngine()
    U.register_field("gravity", DummyField())
    try:
        U.register_field("gravity", DummyField())
    except ValueError as exc:
        assert "already registered" in str(exc)
    else:
        raise AssertionError("Expected duplicate registration to raise")


def test_component_error_wraps_with_context():
    from universe.engine.universe_engine import UniverseEngine

    class BadField:
        def step(self, dt):
            raise RuntimeError("boom")

    U = UniverseEngine()
    U.register_field("bad", BadField())
    try:
        U.step(0.1)
    except RuntimeError as exc:
        assert "field 'bad' failed during 'step'" in str(exc)
    else:
        raise AssertionError("Expected component failure to wrap error")


def test_continue_on_error_logs_and_continues(caplog):
    from universe.engine.universe_engine import UniverseEngine

    class BadPattern:
        def evaluate(self, engine, dt):
            raise RuntimeError("boom")

    class SpyGlyph:
        def __init__(self):
            self.rendered = False

        def render(self, engine):
            self.rendered = True

    U = UniverseEngine(continue_on_error=True)
    U.register_pattern(BadPattern())
    spy = U.register_glyph(SpyGlyph())

    with caplog.at_level(logging.ERROR):
        U.step(0.2)

    assert spy.rendered, "Glyph render should still execute when continue_on_error is True"
    assert any("pattern" in record.message for record in caplog.records)
