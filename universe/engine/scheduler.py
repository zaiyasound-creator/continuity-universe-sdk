class FixedStepScheduler:
    """
    Converts variable frame times into fixed simulation steps with optional smoothing.
    """

    def __init__(self, fixed_dt: float, max_accumulated_steps: int = 8, smoothing: float = 0.1):
        self.fixed_dt = fixed_dt
        self.max_accumulated_steps = max_accumulated_steps
        self.smoothing = smoothing
        self._smoothed_dt = fixed_dt
        self._accumulator = 0.0

    def add_time(self, real_dt: float) -> None:
        # Exponential smoothing to dampen jitter
        self._smoothed_dt = (self._smoothed_dt * (1 - self.smoothing)) + (real_dt * self.smoothing)
        # Clamp to avoid spiral of death
        capped = min(real_dt, self.fixed_dt * self.max_accumulated_steps)
        self._accumulator += capped

    def steps_due(self) -> int:
        steps = 0
        while self._accumulator + 1e-9 >= self.fixed_dt and steps < self.max_accumulated_steps:
            self._accumulator -= self.fixed_dt
            steps += 1
        return steps

    def consume(self, real_dt: float) -> int:
        """
        Add real time and return number of fixed steps to execute.
        """
        self.add_time(real_dt)
        return self.steps_due()
