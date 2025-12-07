import random


class GlyphEvolution:
    """
    Introduces mutation/drift into glyph shapes.
    """

    def mutate(self, glyph):
        if random.random() < 0.05:
            glyph.shape_id = (glyph.shape_id + random.randint(-2, 2)) % 16
        return glyph
