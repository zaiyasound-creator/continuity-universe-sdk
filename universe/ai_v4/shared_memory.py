class SharedMemory:
    """
    Shared event buffer for group gossip.
    """

    def __init__(self):
        self.events = []

    def add(self, event):
        self.events.append(event)
        if len(self.events) > 200:
            self.events.pop(0)

    def sample(self):
        return self.events[-5:] if self.events else []
