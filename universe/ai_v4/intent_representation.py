class IntentRepresentation:
    """
    Stores the current interpreted/group intent.
    """

    def __init__(self):
        self.intent = None

    def update(self, interpreted_intent):
        if interpreted_intent:
            self.intent = interpreted_intent
