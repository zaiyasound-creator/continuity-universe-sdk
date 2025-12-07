import numpy as np


class Climate:
    """
    Basic planetary climate model producing temperature and humidity fields.
    """

    def __init__(self, width: int = 200, height: int = 200):
        self.width = width
        self.height = height
        self.temperature = np.zeros((height, width))
        self.humidity = np.zeros((height, width))

    def update(self, season_shift: float = 0.0):
        for y in range(self.height):
            latitude = abs((y / self.height) - 0.5) * 2.0  # 0 = equator, 1 = poles
            base_temp = (1.0 - latitude) * 30  # equator ~30°C, poles ~0°C
            seasonal = season_shift * 12  # amplitude of seasonal cycle
            self.temperature[y, :] = base_temp + seasonal
            self.humidity[y, :] = (1.0 - latitude) * 0.7 + 0.3
