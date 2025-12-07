import math


class DecisionLayer:
    """
    Converts desire vectors into movement updates.
    """

    def decide(self, agent, dx: float, dy: float, dt: float, speed: float):
        mag = math.sqrt(dx * dx + dy * dy)
        if mag > 0:
            dx /= mag
            dy /= mag

        agent.vx = dx * speed
        agent.vy = dy * speed

        agent.x += agent.vx * dt
        agent.y += agent.vy * dt
