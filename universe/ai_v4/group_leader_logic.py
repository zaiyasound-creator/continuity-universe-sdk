class GroupLeaderLogic:
    """
    Chooses a leader based on stability and sociability.
    """

    def choose_leader(self, agents):
        scored = sorted(
            agents,
            key=lambda a: a.personality.stability + a.personality.sociability,
            reverse=True,
        )
        return scored[0] if scored else None
