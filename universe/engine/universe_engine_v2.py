import asyncio
from copy import deepcopy
from typing import Any, Callable, Dict, List, Optional, Sequence

from universe.systems.base_system import System
from universe.world.world_state import WorldState


class EventBus:
    """
    Lightweight synchronous event bus with deferred dispatch queue.
    """

    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Any], Any]]] = {}
        self._queue: List[tuple[str, Any]] = []

    def subscribe(self, event_type: str, handler: Callable[[Any], Any]) -> None:
        self._subscribers.setdefault(event_type, []).append(handler)

    def publish(self, event_type: str, payload: Any = None) -> None:
        self._queue.append((event_type, payload))

    def flush(self) -> None:
        while self._queue:
            event_type, payload = self._queue.pop(0)
            for handler in self._subscribers.get(event_type, []):
                result = handler(payload)
                if asyncio.iscoroutine(result):
                    asyncio.run(result)


class UniverseEngineV2:
    """
    ECS-oriented Universe Engine with detachable physics pipeline, event bus,
    deterministic tick order, and reversible time stepping.
    """

    PHASE_ORDER: Sequence[str] = ("physics", "patterns", "logic", "glyphs")

    def __init__(self, history_limit: int = 256, continue_on_error: bool = False):
        self.world = WorldState()
        self.event_bus = EventBus()
        self._systems: Dict[str, List[System]] = {phase: [] for phase in self.PHASE_ORDER}
        self._history: List[Dict[str, Any]] = []
        self._history_limit = max(1, history_limit)
        self._in_tick = False
        self.physics_enabled = True
        self.continue_on_error = continue_on_error

    # Subsystem registration -------------------------------------------------
    def register_system(self, system: System, phase: Optional[str] = None) -> System:
        phase_name = phase or getattr(system, "phase", "logic")
        if phase_name not in self._systems:
            raise ValueError(f"Unknown phase '{phase_name}'")
        self._systems[phase_name].append(system)
        # Keep deterministic ordering by stable sort on system.order
        self._systems[phase_name].sort(key=lambda s: getattr(s, "order", 0))
        return system

    def register_physics_system(self, system: System) -> System:
        system.phase = "physics"
        return self.register_system(system, phase="physics")

    def register_pattern_system(self, system: System) -> System:
        system.phase = "patterns"
        return self.register_system(system, phase="patterns")

    def register_glyph_system(self, system: System) -> System:
        system.phase = "glyphs"
        return self.register_system(system, phase="glyphs")

    # State management -------------------------------------------------------
    def snapshot_state(self) -> Dict[str, Any]:
        return {
            "world": self.world.snapshot(),
        }

    def restore_state(self, snapshot: Dict[str, Any]) -> None:
        self.world.restore(deepcopy(snapshot["world"]))

    def _push_history(self) -> None:
        self._history.append(self.snapshot_state())
        if len(self._history) > self._history_limit:
            self._history.pop(0)

    def rewind(self, steps: int = 1) -> float:
        if steps < 1 or steps > len(self._history):
            raise ValueError("Cannot rewind that many steps")
        snapshot = self._history[-steps]
        self.restore_state(snapshot)
        # Drop consumed snapshots
        self._history = self._history[:-steps]
        return self.world.time

    # Tick execution ---------------------------------------------------------
    def _execute_system(self, system: System, dt: float) -> None:
        result = system.update(self.world, dt)
        if asyncio.iscoroutine(result):
            asyncio.run(result)

    def _tick_phase(self, phase: str, dt: float) -> None:
        if phase == "physics" and not self.physics_enabled:
            return
        for system in self._systems.get(phase, []):
            try:
                self._execute_system(system, dt)
            except Exception as exc:
                if not self.continue_on_error:
                    raise
                # Continue but emit event for observability
                self.event_bus.publish("system_error", {"phase": phase, "system": system.name, "error": exc})

    def step(self, dt: float = 1.0) -> float:
        if self._in_tick:
            raise RuntimeError("Re-entrant tick detected")

        if dt < 0:
            return self.rewind(steps=1)

        self._push_history()
        self._in_tick = True
        try:
            self.world.advance_time(dt)
            for phase in self.PHASE_ORDER:
                self._tick_phase(phase, dt)
            self.event_bus.flush()
        finally:
            self._in_tick = False
        return self.world.time

    def run(self, steps: int = 1, dt: float = 1.0) -> float:
        for _ in range(steps):
            self.step(dt)
        return self.world.time

    # Utilities --------------------------------------------------------------
    def detach_physics(self) -> None:
        self.physics_enabled = False

    def attach_physics(self) -> None:
        self.physics_enabled = True
