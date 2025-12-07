class Scheduler:
    """
    Fixed-step scheduler for physics-like updates.
    """

    def __init__(self, fixed_dt: float = 0.016):
        self.fixed_dt = fixed_dt
        self.accumulator = 0.0

    def tick(self, dt: float) -> int:
        """
        Add real time and return number of fixed updates to execute.
        """
        self.accumulator += dt
        count = 0
        while self.accumulator >= self.fixed_dt:
            self.accumulator -= self.fixed_dt
            count += 1
        return count
