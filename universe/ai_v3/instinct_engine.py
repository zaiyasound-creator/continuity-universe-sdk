import math


class InstinctEngine:
    """
    Instinctual steering from emotional states and personality.
    """

    def instincts(self, agent, emotion, personality):
        dx = dy = 0.0

        dx += emotion.fear * personality.caution * -agent.vx
        dy += emotion.fear * personality.caution * -agent.vy

        dx += personality.wanderlust * (math.copysign(1, agent.vx if agent.vx != 0 else 1.0) * 0.3)
        dy += personality.wanderlust * (math.copysign(1, agent.vy if agent.vy != 0 else 1.0) * 0.3)

        dx *= emotion.calm
        dy *= emotion.calm

        return dx, dy
