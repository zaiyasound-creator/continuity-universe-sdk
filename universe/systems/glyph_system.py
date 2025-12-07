from universe.components.glyph_component import GlyphComponent
from universe.components.position import Position
from universe.systems.base_system import System


class GlyphSystem(System):
    """
    Invokes glyph rendering hooks for entities that have glyph data.
    """

    def __init__(self, name: str = "glyphs", order: int = 100, phase: str = "glyphs"):
        super().__init__(name=name, order=order, phase=phase)

    def update(self, world, dt: float):
        for entity in world.all_entities():
            glyph_comp = entity.get_component(GlyphComponent)
            if glyph_comp is None:
                continue
            glyph = glyph_comp.glyph
            renderer = getattr(glyph, "render_entity", None) or getattr(glyph, "render", None)
            if callable(renderer):
                pos = entity.get_component(Position)
                renderer(entity, pos)
