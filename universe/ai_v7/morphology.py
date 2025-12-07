class Morphology:
    """
    Handles affixes, intensifiers, and compound-glyph construction.
    """

    def inflect(self, base_glyph, emotion, intensity: float):
        new_shape = (base_glyph.shape_id + int(intensity * 3)) % 16
        new_tag = base_glyph.tag + "_strong" if intensity > 0.7 else base_glyph.tag
        return new_shape, new_tag
