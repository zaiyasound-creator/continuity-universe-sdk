from universe.ai_v2.decision_layer import DecisionLayer
from universe.ai_v2.group_behavior import GroupBehavior


class CognitionCPU:
    """
    CPU cognition driver for agents.
    """

    def __init__(self, speed: float = 1.2):
        self.speed = speed
        self.group = GroupBehavior()
        self.decider = DecisionLayer()

    def step(self, agents, sigma, ache, kappa, phi_x, phi_y, dt: float):
        h, w = sigma.shape

        for a in agents:
            x = int(a.x) % w
            y = int(a.y) % h

            local_sigma = sigma[y, x]
            local_ache = ache[y, x]
            local_kappa = kappa[y, x]

            a.brain.memory.record(local_sigma, local_ache, local_kappa)

            dx, dy = a.brain.compute_desire(
                local_sigma,
                local_ache,
                local_kappa,
                phi_x[y, x],
                phi_y[y, x],
            )

            neighbors = [n for n in agents if n.id != a.id]
            gdx, gdy = self.group.apply(a, neighbors)

            dx += gdx
            dy += gdy

            self.decider.decide(a, dx, dy, dt, self.speed)
