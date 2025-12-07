import math


class Light:
    def __init__(self, x: float, y: float, intensity: float = 1.0, radius: float = 10.0, color=(255, 255, 200)):
        self.x = x
        self.y = y
        self.intensity = intensity
        self.radius = radius
        self.color = color


class LightingEngine:
    def __init__(self):
        self.lights = []

    def add_light(self, light: Light):
        self.lights.append(light)

    def sample(self, x: float, y: float):
        """Returns brightness [0..1] and blended light color."""
        brightness = 0.0
        r = g = b = 0.0

        for L in self.lights:
            dx = x - L.x
            dy = y - L.y
            d = math.sqrt(dx * dx + dy * dy)

            if d < L.radius:
                falloff = (1 - d / L.radius) * L.intensity
                brightness += falloff
                r += L.color[0] * falloff
                g += L.color[1] * falloff
                b += L.color[2] * falloff

        if brightness > 1:
            brightness = 1

        if brightness == 0:
            return 0.0, (0, 0, 0)

        return brightness, (int(r / brightness), int(g / brightness), int(b / brightness))
