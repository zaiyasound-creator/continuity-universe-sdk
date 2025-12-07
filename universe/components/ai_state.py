class AIState:
    """Finite state for simple AI behaviors."""

    def __init__(self, state: str = "idle"):
        self.state = state
        self.timer = 0.0
