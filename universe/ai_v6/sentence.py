class Sentence:
    """
    Sequence of glyphs forming a sentence.
    """

    def __init__(self, glyphs):
        self.glyphs = glyphs

    def __repr__(self):
        return "Sentence(" + ", ".join(f"{g.tag}:{g.shape_id}" for g in self.glyphs) + ")"
