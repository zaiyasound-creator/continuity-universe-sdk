class DialectEngine:
    """
    Applies region-specific bias to glyph shapes.
    """

    def __init__(self, region_bias: int):
        self.bias = region_bias

    def apply(self, glyph):
        glyph.shape_id = (glyph.shape_id + self.bias) % 16
        return glyph
