def test_full_engine_integration():
    from universe.engine.universe_engine import UniverseEngine
    from physics.simple_gravity import SimpleGravityField
    from patterns.coherence_stabilizer import CoherenceStabilizerPattern
    from glyphs.console_status import ConsoleStatusGlyph

    U = UniverseEngine()

    U.register_field("gravity", SimpleGravityField())
    U.register_pattern(CoherenceStabilizerPattern())
    U.register_glyph(ConsoleStatusGlyph(every_n_steps=1000))  # prevent spam

    U.run(steps=5, dt=0.1)

    # Engine must progress time
    assert U.time == 0.5

    # Gravity field should have updated
    assert U.fields["gravity"].position != 0.0
