class CommunicationProtocol:
    """
    Interprets incoming signals into movement biases and intent.
    """

    def interpret(self, agent, signals):
        dx = dy = 0.0
        intent = None

        for s in signals:
            if s.type == "danger":
                dx += (agent.x - s.x) * 0.02
                dy += (agent.y - s.y) * 0.02
                intent = "flee"
            elif s.type == "gather":
                dx += (s.x - agent.x) * 0.01
                dy += (s.y - agent.y) * 0.01
                intent = "gather"
            elif s.type == "migrate":
                intent = "migrate"

        return dx, dy, intent
