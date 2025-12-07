from universe.ai_v6.sentence import Sentence


class Glyph:
    """
    Symbolic language unit with shape, intensity, and semantic tag.
    Compatible with AI Packs 5–7 (grammar, morphology, phonology, dialect, evolution).
    """

    def __init__(self, shape_id: int, intensity: float = 1.0, tag: str = ""):
        self.shape_id = shape_id
        self.intensity = intensity
        self.tag = tag

    def clone(self):
        """
        Produce a safe copy for mutation/dialect engines.
        Prevents corruption of base lexicon glyphs.
        """
        return Glyph(self.shape_id, self.intensity, self.tag)


class Composer:
    """
    Converts word tokens into glyph objects and produces Sentence objects.
    """

    def compose(self, words, lexicon):
        glyphs = []
        for w in words:
            shape = lexicon.get_shape(w)
            if shape is None:
                continue
            glyphs.append(Glyph(shape_id=shape, intensity=1.0, tag=w))
        return Sentence(glyphs)
