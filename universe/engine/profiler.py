import time
from collections import defaultdict
from typing import Dict, List


class EngineProfiler:
    """
    Collects per-system and per-tick timing metrics.
    """

    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self.tick_durations: List[float] = []
        self.system_durations: Dict[str, float] = defaultdict(float)
        self._tick_start: float = 0.0

    def start_tick(self) -> None:
        self._tick_start = time.perf_counter()

    def end_tick(self) -> None:
        if self._tick_start:
            duration = time.perf_counter() - self._tick_start
            self.tick_durations.append(duration)
        self._tick_start = 0.0

    def record_system(self, system_name: str, duration: float) -> None:
        self.system_durations[system_name] += duration

    def last_tick_ms(self) -> float:
        return (self.tick_durations[-1] * 1000) if self.tick_durations else 0.0

    def average_tick_ms(self) -> float:
        if not self.tick_durations:
            return 0.0
        return sum(self.tick_durations) * 1000 / len(self.tick_durations)
