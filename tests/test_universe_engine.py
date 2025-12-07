def test_engine_boot():
    from universe.engine.universe_engine import UniverseEngine
    U = UniverseEngine()
    assert U.time == 0
