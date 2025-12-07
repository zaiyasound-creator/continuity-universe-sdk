import numpy as np


class GroupBehavior:
    """
    Flocking-style group influence (cohesion, alignment, separation).
    """

    def __init__(self, cohesion: float = 0.03, alignment: float = 0.04, separation: float = 0.08, radius: float = 10.0):
        self.cohesion = cohesion
        self.alignment = alignment
        self.separation = separation
        self.radius = radius

    def apply(self, agent, neighbors):
        if not neighbors:
            return 0.0, 0.0

        cx = np.mean([n.x for n in neighbors])
        cy = np.mean([n.y for n in neighbors])
        ax = np.mean([n.vx for n in neighbors])
        ay = np.mean([n.vy for n in neighbors])

        dx = (cx - agent.x) * self.cohesion + ax * self.alignment
        dy = (cy - agent.y) * self.cohesion + ay * self.alignment

        for n in neighbors:
            dist2 = (agent.x - n.x) ** 2 + (agent.y - n.y) ** 2
            if dist2 < self.radius * self.radius:
                dx += (agent.x - n.x) * self.separation
                dy += (agent.y - n.y) * self.separation

        return dx, dy
