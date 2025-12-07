class DecisionV3:
    """
    Combines desires, memory, and role to set agent movement.
    """

    def __init__(self):
        pass

    def decide(self, agent, dx: float, dy: float, emotion, memory, role: str):
        prefs = memory.preferred_locations()
        if prefs and role != "scout":
            px, py, _ = prefs[0]
            dx += (px - agent.x) * 0.001
            dy += (py - agent.y) * 0.001

        if role == "protector":
            dx *= 0.5
            dy *= 0.5
        if role == "scout":
            dx *= 1.4
            dy *= 1.4

        agent.vx = dx
        agent.vy = dy
