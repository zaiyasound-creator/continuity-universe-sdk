class SemanticFrame:
    """
    Maps parsed meaning into emotion/behavior adjustments.
    """

    def interpret(self, tree, agent):
        meaning = tree.meaning()

        action = meaning.get("action")
        if action == "danger":
            if hasattr(agent, "emotion"):
                agent.emotion.fear += 0.1
        if action == "gather":
            agent.intent = "gather"
        if action == "migrate":
            agent.intent = "migrate"

        subject = meaning.get("subject")
        if subject == "leader":
            agent.obey_leader = True
