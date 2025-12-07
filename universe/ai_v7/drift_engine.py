import random


class DriftEngine:
    """
    Slowly shifts grammar/lexicon over time.
    """

    def drift_syntax(self, grammar):
        if hasattr(grammar, "word_order"):
            options = ["SVO", "OSV", "VSO"]
            grammar.word_order = random.choice(options)
