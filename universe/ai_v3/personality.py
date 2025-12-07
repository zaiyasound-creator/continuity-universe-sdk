import random


class Personality:
    """
    Personality vector influencing risk, exploration, sociability, and stability.
    """

    def __init__(
        self,
        curiosity: float = 1.0,
        caution: float = 1.0,
        sociability: float = 1.0,
        stability: float = 1.0,
        wanderlust: float = 1.0,
    ):
        self.curiosity = curiosity + random.uniform(-0.3, 0.3)
        self.caution = caution + random.uniform(-0.3, 0.3)
        self.sociability = sociability + random.uniform(-0.3, 0.3)
        self.stability = stability + random.uniform(-0.3, 0.3)
        self.wanderlust = wanderlust + random.uniform(-0.3, 0.3)
