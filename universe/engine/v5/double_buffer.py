class DoubleBuffer:
    """
    Simple double buffer for thread-safe swap of shared state.
    """

    def __init__(self):
        self.front = {}
        self.back = {}

    def swap(self):
        self.front, self.back = self.back, self.front
        self.back.clear()
