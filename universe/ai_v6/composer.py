from universe.ai_v6.sentence import Sentence


class Glyph:
    """
    Minimal glyph representation used for language composition.
    """

    def __init__(self, shape_id: int, intensity: float = 1.0, tag: str = ""):
        self.shape_id = shape_id
        self.intensity = intensity
        self.tag = tag


class Composer:
    """
    Converts words into glyphs and produces sentences.
    """

    def compose(self, words, lexicon):
        glyphs = []
        for w in words:
            shape = lexicon.get_shape(w)
            if shape is None:
                continue
            glyphs.append(Glyph(shape, intensity=1.0, tag=w))
        return Sentence(glyphs)
