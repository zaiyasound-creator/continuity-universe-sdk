class AgentMemory:
    """
    Short-term memory of local field samples.
    """

    def __init__(self, size: int = 8):
        self.size = size
        self.history = []

    def record(self, sigma, ache, kappa):
        self.history.append((sigma, ache, kappa))
        if len(self.history) > self.size:
            self.history.pop(0)

    def trend(self):
        if len(self.history) < 2:
            return 0, 0, 0
        ds = self.history[-1][0] - self.history[0][0]
        da = self.history[-1][1] - self.history[0][1]
        dk = self.history[-1][2] - self.history[0][2]
        return ds, da, dk
