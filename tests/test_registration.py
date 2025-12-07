def test_register_field():
    from universe.engine.universe_engine import UniverseEngine
    U = UniverseEngine()

    class F: pass
    f = F()
    U.register_field("f", f)

    assert "f" in U.fields
    assert U.fields["f"] == f


def test_register_pattern():
    from universe.engine.universe_engine import UniverseEngine
    U = UniverseEngine()

    class P: pass
    p = P()
    U.register_pattern(p)

    assert p in U.patterns


def test_register_glyph():
    from universe.engine.universe_engine import UniverseEngine
    U = UniverseEngine()

    class G: pass
    g = G()
    U.register_glyph(g)

    assert g in U.glyphs
