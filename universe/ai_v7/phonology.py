class Phonology:
    """
    Converts rhythmic patterns (emotion-driven) into glyph-shape modifiers.
    """

    def prosody_shift(self, glyph, emotion):
        shift = int(emotion.fear * 4 - emotion.excitement * 2)
        return (glyph.shape_id + shift) % 16
