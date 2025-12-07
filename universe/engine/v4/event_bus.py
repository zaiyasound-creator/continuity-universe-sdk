class EventBus:
    """Publish/subscribe event bus."""

    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_name, fn):
        self.listeners.setdefault(event_name, []).append(fn)

    def publish(self, event_name, payload=None):
        for fn in self.listeners.get(event_name, []):
            fn(payload)
