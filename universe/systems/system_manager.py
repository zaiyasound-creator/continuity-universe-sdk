import asyncio
import time
from typing import Dict, Iterable, List, Optional

from universe.engine.event_bus import EventBus
from universe.engine.profiler import EngineProfiler
from universe.systems.base_system import System
from universe.world.world_state import WorldState


class SystemManager:
    """
    Registers and executes systems in deterministic phase/order.
    """

    PHASE_ORDER: List[str] = [
        "physics_before",
        "physics",
        "physics_after",
        "patterns",
        "logic",
        "glyphs",
    ]

    def __init__(self, continue_on_error: bool = False):
        self._systems: Dict[str, List[System]] = {phase: [] for phase in self.PHASE_ORDER}
        self.continue_on_error = continue_on_error

    def register(self, system: System, phase: Optional[str] = None) -> System:
        phase_name = phase or getattr(system, "phase", "logic")
        if phase_name not in self._systems:
            raise ValueError(f"Unknown phase '{phase_name}'")
        self._systems[phase_name].append(system)
        # Deterministic ordering: order then name for stability
        self._systems[phase_name].sort(key=lambda s: (getattr(s, "order", 0), getattr(s, "name", "")))
        return system

    def systems_for(self, phase: str) -> Iterable[System]:
        return self._systems.get(phase, [])

    def update(
        self,
        world: WorldState,
        dt: float,
        profiler: Optional[EngineProfiler] = None,
        event_bus: Optional[EventBus] = None,
        physics_enabled: bool = True,
    ) -> None:
        for phase in self.PHASE_ORDER:
            if phase.startswith("physics") and not physics_enabled:
                continue
            for system in self._systems.get(phase, []):
                start = time.perf_counter()
                try:
                    result = system.update(world, dt)
                    if asyncio.iscoroutine(result):
                        asyncio.run(result)
                except Exception as exc:
                    if event_bus:
                        event_bus.publish(
                            "system_error",
                            {"phase": phase, "system": getattr(system, "name", ""), "error": exc},
                        )
                    if not self.continue_on_error:
                        raise
                finally:
                    if profiler:
                        profiler.record_system(getattr(system, "name", phase), time.perf_counter() - start)
