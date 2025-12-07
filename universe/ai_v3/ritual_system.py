import numpy as np


class RitualSystem:
    """
    Ritual swarm behaviors triggered by high sigma regions.
    """

    def __init__(self, trigger_sigma: float = 150.0):
        self.trigger_sigma = trigger_sigma

    def check(self, sigma: np.ndarray, x: int, y: int) -> bool:
        return sigma[y, x] > self.trigger_sigma

    def ritual_vector(self, agent, group):
        dx = np.sin(agent.id * 0.7) * 0.5
        dy = np.cos(agent.id * 0.7) * 0.5
        return dx, dy
