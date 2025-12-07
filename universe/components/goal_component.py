class GoalComponent:
    """Simple goal holder for GOAP-like behaviors."""

    def __init__(self, goal_fn):
        self.goal_fn = goal_fn
        self.progress = 0.0
