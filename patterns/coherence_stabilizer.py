class CoherenceStabilizerPattern:
    """
    Dummy pattern that would normally modulate fields; here it just records calls.
    """

    def __init__(self):
        self.evaluations = 0

    def evaluate(self, engine, dt: float) -> None:
        self.evaluations += 1
