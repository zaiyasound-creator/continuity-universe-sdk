import logging
from typing import Any, Dict, List, Optional, Protocol, Tuple


logger = logging.getLogger(__name__)


class FieldLike(Protocol):
    def step(self, dt: float) -> Any: ...

    def update(self, dt: float) -> Any: ...

    def bind_universe(self, engine: "UniverseEngine") -> None: ...


class PatternLike(Protocol):
    def evaluate(self, engine: "UniverseEngine", dt: float) -> Any: ...

    def step(self, dt: float) -> Any: ...

    def bind_universe(self, engine: "UniverseEngine") -> None: ...


class GlyphLike(Protocol):
    def render(self, engine: "UniverseEngine") -> Any: ...

    def draw(self, engine: "UniverseEngine") -> Any: ...

    def bind_universe(self, engine: "UniverseEngine") -> None: ...


class UniverseEngine:
    """
    Main loop coordinator for the Continuity Universe simulation.

    Phases per step:
    1) physics field updates
    2) pattern evaluation
    3) glyph rendering/hooks
    """

    def __init__(self, continue_on_error: bool = False):
        self.time: float = 0.0
        self.fields: Dict[str, FieldLike] = {}
        self.patterns: List[PatternLike] = []
        self.glyphs: List[GlyphLike] = []
        self.running: bool = False
        self.continue_on_error: bool = continue_on_error

    def register_field(self, name: str, field: FieldLike) -> FieldLike:
        """
        Attach a physics field to the universe under a stable name.
        """
        if name in self.fields:
            raise ValueError(f"Field '{name}' already registered")
        self.fields[name] = field
        self._bind_component(field)
        return field

    def register_pattern(self, pattern: PatternLike) -> PatternLike:
        """
        Attach a pattern object that will be evaluated each step.
        """
        self.patterns.append(pattern)
        self._bind_component(pattern)
        return pattern

    def register_glyph(self, glyph: GlyphLike) -> GlyphLike:
        """
        Attach a glyph object that will be invoked after updates.
        """
        self.glyphs.append(glyph)
        self._bind_component(glyph)
        return glyph

    def get_field(self, name: str) -> Optional[FieldLike]:
        return self.fields.get(name)

    def _bind_component(self, component: Any) -> None:
        binder = getattr(component, "bind_universe", None)
        if callable(binder):
            binder(self)

    def _advance_time(self, dt: float) -> None:
        self.time += dt

    def _update_fields(self, dt: float) -> None:
        for name, field in self.fields.items():
            self._invoke_component("field", name, field, ("step", "update"), dt)

    def _update_patterns(self, dt: float) -> None:
        for idx, pattern in enumerate(self.patterns):
            name = getattr(pattern, "name", None) or f"pattern[{idx}]"
            self._invoke_component("pattern", name, pattern, ("evaluate", "step"), self, dt)

    def _render_glyphs(self) -> None:
        for idx, glyph in enumerate(self.glyphs):
            name = getattr(glyph, "name", None) or f"glyph[{idx}]"
            self._invoke_component("glyph", name, glyph, ("render", "draw"), self)

    def _invoke_component(
        self,
        kind: str,
        name: str,
        component: Any,
        candidates: Tuple[str, ...],
        *args: Any,
    ) -> None:
        for attr in candidates:
            handler = getattr(component, attr, None)
            if callable(handler):
                try:
                    handler(*args)
                except Exception as exc:
                    message = f"{kind} '{name}' failed during '{attr}'"
                    if self.continue_on_error:
                        logger.exception(message)
                        return
                    raise RuntimeError(message) from exc
                return

    def step(self, dt: float = 1.0) -> float:
        """
        Advance simulation time and execute a full update/render pass.
        """
        if dt < 0:
            raise ValueError("dt must be non-negative")

        self._advance_time(dt)
        self._update_fields(dt)
        self._update_patterns(dt)
        self._render_glyphs()
        return self.time

    def run(self, steps: int = 1, dt: float = 1.0) -> float:
        """
        Run the engine for a number of steps, keeping the loop stateful.
        """
        if self.running:
            raise RuntimeError("Engine is already running")

        self.running = True
        try:
            for _ in range(steps):
                self.step(dt)
        finally:
            self.running = False
        return self.time


if __name__ == "__main__":
    engine = UniverseEngine()
    print("Universe Online:", engine.time)
    engine.run(steps=3, dt=0.5)
    print("After run:", engine.time)
