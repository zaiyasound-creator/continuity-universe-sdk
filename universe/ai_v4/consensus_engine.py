class ConsensusEngine:
    """
    Majority-rule consensus over agents' intents.
    """

    def decide(self, agents):
        intents = [getattr(a.intent, "intent", None) for a in agents if getattr(a.intent, "intent", None)]
        if not intents:
            return None
        counts = {}
        for i in intents:
            counts[i] = counts.get(i, 0) + 1
        return max(counts, key=counts.get)
