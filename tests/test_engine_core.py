def test_engine_boot():
    from universe.engine.universe_engine import UniverseEngine
    U = UniverseEngine()
    assert U.time == 0.0


def test_engine_step_accumulates_time():
    from universe.engine.universe_engine import UniverseEngine
    U = UniverseEngine()
    U.step(0.5)
    assert U.time == 0.5


def test_engine_run_multiple_steps():
    from universe.engine.universe_engine import UniverseEngine
    U = UniverseEngine()
    U.run(steps=4, dt=0.25)
    assert U.time == 1.0
