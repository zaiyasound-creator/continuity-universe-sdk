from universe.components.base_component import Component


class GlyphComponent(Component):
    """Attach rendering/glyph data to an entity."""

    def __init__(self, glyph):
        self.glyph = glyph
