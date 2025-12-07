import math


class Easing:
    @staticmethod
    def smoothstep(t: float) -> float:
        return t * t * (3 - 2 * t)

    @staticmethod
    def ease_out(t: float) -> float:
        return 1 - (1 - t) ** 3

    @staticmethod
    def ease_in(t: float) -> float:
        return t * t * t

    @staticmethod
    def ease_in_out(t: float) -> float:
        return 0.5 * (math.sin((t - 0.5) * math.pi) + 1)
