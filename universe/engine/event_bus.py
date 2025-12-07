import asyncio
from typing import Any, Callable, Dict, List


class EventBus:
    """
    Simple publish/subscribe event bus with deferred dispatch.
    Supports async handlers by auto-running coroutines.
    """

    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Any], Any]]] = {}
        self._queue: List[tuple[str, Any]] = []

    def subscribe(self, event_type: str, handler: Callable[[Any], Any]) -> None:
        self._subscribers.setdefault(event_type, []).append(handler)

    def publish(self, event_type: str, payload: Any = None) -> None:
        self._queue.append((event_type, payload))

    def flush(self) -> None:
        """
        Dispatch all queued events synchronously; awaits coroutines automatically.
        """
        while self._queue:
            event_type, payload = self._queue.pop(0)
            for handler in self._subscribers.get(event_type, []):
                result = handler(payload)
                if asyncio.iscoroutine(result):
                    asyncio.run(result)
