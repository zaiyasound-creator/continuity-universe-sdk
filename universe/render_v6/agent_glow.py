import numpy as np


class AgentGlow:
    """
    Adds glowing spots around agent positions.
    """

    def __init__(self, radius: int = 3, intensity: int = 255):
        self.radius = radius
        self.intensity = intensity

    def apply(self, frame: np.ndarray, agents) -> np.ndarray:
        img = frame.copy()
        h, w, _ = img.shape

        for a in agents:
            x = int(getattr(a, "x", 0) if hasattr(a, "x") else getattr(a, "pos", (0, 0))[0]) % w
            y = int(getattr(a, "y", 0) if hasattr(a, "y") else getattr(a, "pos", (0, 0))[1]) % h

            for dy in range(-self.radius, self.radius + 1):
                for dx in range(-self.radius, self.radius + 1):
                    if dx * dx + dy * dy <= self.radius * self.radius:
                        img[(y + dy) % h, (x + dx) % w] = [self.intensity, self.intensity, self.intensity]

        return img
