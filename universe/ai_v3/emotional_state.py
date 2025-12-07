class EmotionalState:
    """
    Dynamic mood engine influenced by local fields and personality.
    """

    def __init__(self):
        self.fear = 0.0
        self.excitement = 0.0
        self.calm = 1.0

    def update(self, local_sigma: float, local_ache: float, personality):
        self.calm += local_sigma * 0.01
        self.excitement += local_sigma * 0.005
        self.fear += local_ache * 0.02 * (2.0 - personality.stability)

        self.calm *= 0.98
        self.excitement *= 0.96
        self.fear *= 0.95
