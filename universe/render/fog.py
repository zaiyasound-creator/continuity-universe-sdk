class Fog:
    """Simple distance fog color blending."""

    def __init__(self, density: float = 0.05, color=(50, 50, 80)):
        self.density = density
        self.color = color

    def apply(self, r: int, g: int, b: int, distance: float):
        fog_factor = 1 - (1 / (1 + self.density * max(distance, 0)))
        r = int(r * (1 - fog_factor) + self.color[0] * fog_factor)
        g = int(g * (1 - fog_factor) + self.color[1] * fog_factor)
        b = int(b * (1 - fog_factor) + self.color[2] * fog_factor)
        return r, g, b
