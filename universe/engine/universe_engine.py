class UniverseEngine:
    """
    Main loop coordinator for the Continuity Universe simulation.

    The engine tracks simulation time and orchestrates three phases per step:
    1) physics field updates
    2) pattern evaluation
    3) glyph rendering/hooks

    The concrete field, pattern, and glyph objects are intentionally loose:
    - physics fields are expected to expose a ``step(dt)`` or ``update(dt)`` method
    - patterns are expected to expose ``evaluate(engine, dt)`` (or ``step(dt)``)
    - glyphs are expected to expose ``render(engine)`` (or ``draw(engine)``)
    """

    def __init__(self):
        self.time = 0.0
        self.fields = {}
        self.patterns = []
        self.glyphs = []
        self.running = False

    def register_field(self, name, field):
        """
        Attach a physics field to the universe under a stable name.
        """
        self.fields[name] = field
        binder = getattr(field, "bind_universe", None)
        if callable(binder):
            binder(self)
        return field

    def register_pattern(self, pattern):
        """
        Attach a pattern object that will be evaluated each step.
        """
        self.patterns.append(pattern)
        binder = getattr(pattern, "bind_universe", None)
        if callable(binder):
            binder(self)
        return pattern

    def register_glyph(self, glyph):
        """
        Attach a glyph object that will be invoked after updates.
        """
        self.glyphs.append(glyph)
        binder = getattr(glyph, "bind_universe", None)
        if callable(binder):
            binder(self)
        return glyph

    def _advance_time(self, dt):
        self.time += dt

    def _update_fields(self, dt):
        for field in self.fields.values():
            updater = getattr(field, "step", None) or getattr(field, "update", None)
            if callable(updater):
                updater(dt)

    def _update_patterns(self, dt):
        for pattern in self.patterns:
            evaluator = getattr(pattern, "evaluate", None) or getattr(pattern, "step", None)
            if callable(evaluator):
                evaluator(self, dt)

    def _render_glyphs(self):
        for glyph in self.glyphs:
            renderer = getattr(glyph, "render", None) or getattr(glyph, "draw", None)
            if callable(renderer):
                renderer(self)

    def step(self, dt=1.0):
        """
        Advance simulation time and execute a full update/render pass.
        """
        self._advance_time(dt)
        self._update_fields(dt)
        self._update_patterns(dt)
        self._render_glyphs()
        return self.time

    def run(self, steps=1, dt=1.0):
        """
        Run the engine for a number of steps, keeping the loop stateful.
        """
        self.running = True
        for _ in range(steps):
            self.step(dt)
        self.running = False
        return self.time


if __name__ == "__main__":
    engine = UniverseEngine()
    print("Universe Online:", engine.time)
    engine.run(steps=3, dt=0.5)
    print("After run:", engine.time)
