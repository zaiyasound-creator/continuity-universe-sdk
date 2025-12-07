from universe.components.glyph_component import GlyphComponent
from universe.components.position import Position
from universe.render.ascii_renderer import ASCIIRenderer
from universe.systems.base_system import System


class RenderSystem(System):
    """
    Simple ECS rendering system using the ASCII renderer.
    """

    def __init__(self, width: int = 80, height: int = 40, name: str = "render", order: int = 200, phase: str = "glyphs"):
        super().__init__(name=name, order=order, phase=phase)
        self.renderer = ASCIIRenderer(width, height)

    def update(self, world, dt: float):
        self.renderer.clear()
        for entity in world.all_entities():
            pos = entity.get_component(Position)
            glyph = entity.get_component(GlyphComponent)
            if pos and glyph:
                self.renderer.draw_point(int(pos.x), int(pos.y), glyph.glyph)
        self.renderer.render()
