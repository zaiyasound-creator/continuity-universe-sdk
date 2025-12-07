import numpy as np


class SeasonalMigration:
    """
    Seasonal preferred latitude that oscillates over time.
    """

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.phase = 0.0

    def update(self, dt: float):
        self.phase += dt * 0.02

    def preferred_latitude(self) -> float:
        return (self.height / 2) + (self.height / 4) * np.sin(self.phase)
