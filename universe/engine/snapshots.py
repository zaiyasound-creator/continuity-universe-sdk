from copy import deepcopy
from typing import Any, Dict, List, Optional


class SnapshotManager:
    """
    Maintains reversible snapshots for worlds/universes.
    """

    def __init__(self, limit: int = 256, checkpoint_interval: int = 1):
        self.limit = max(1, limit)
        self.checkpoint_interval = max(1, checkpoint_interval)
        self._history: List[Dict[str, Any]] = []
        self._tick_counter: int = 0

    def push(self, state: Dict[str, Any]) -> None:
        self._history.append(deepcopy(state))
        if len(self._history) > self.limit:
            self._history.pop(0)
        self._tick_counter += 1

    def checkpoint(self, state: Dict[str, Any]) -> None:
        if self._tick_counter % self.checkpoint_interval == 0:
            self.push(state)

    def rollback(self, steps: int = 1) -> Dict[str, Any]:
        if steps < 1 or steps > len(self._history):
            raise ValueError("Invalid rollback length")
        target = self._history[-steps]
        # Trim consumed snapshots
        self._history = self._history[:-steps]
        return deepcopy(target)

    def clear(self) -> None:
        self._history.clear()
        self._tick_counter = 0
