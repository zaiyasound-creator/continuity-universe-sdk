class Lexicon:
    """
    Mapping of core concepts to glyph shapes. Extendable over time.
    """

    BASE = {
        "danger": 1,
        "safe": 2,
        "migrate": 3,
        "gather": 4,
        "storm": 5,
        "coherence": 6,
        "ache": 7,
        "leader": 8,
        "you": 9,
        "group": 10,
    }

    def get_shape(self, word):
        return self.BASE.get(word, None)
