class SocialRoles:
    """
    Assign roles based on neighbor count and personality.
    """

    def assign(self, agent, neighbors, personality):
        if personality.sociability < 0.8:
            return "wanderer"

        if len(neighbors) > 5:
            if personality.curiosity > 1.1:
                return "scout"
            if personality.caution > 1.1:
                return "protector"
            return "follower"

        return "leader"
