from universe.components.glyph_component import GlyphComponent
from universe.components.position import Position
from universe.render.camera_system import CameraSystem
from universe.render.layered_renderer import LayeredRenderer
from universe.render.render_pipeline import RenderPipeline
from universe.render.tilemap_renderer import TilemapRenderer
from universe.systems.base_system import System


class RenderSystemV2(System):
    """
    Layered, camera-driven renderer with parallax and pipeline stages.
    """

    def __init__(self, universe, tilemap, animations=None, name: str = "render_v2", order: int = 200, phase: str = "glyphs"):
        super().__init__(name=name, order=order, phase=phase)
        self.camera_system = CameraSystem(universe)
        self.tilemap = TilemapRenderer(tilemap, animations)
        self.pipeline = RenderPipeline()
        self.renderer = None

    def update(self, world, dt: float):
        cam = self.camera_system.camera
        self.renderer = LayeredRenderer(cam)

        self.pipeline.pre.clear()
        self.pipeline.layers.clear()
        self.pipeline.post.clear()

        # background layer
        self.pipeline.add_layer(lambda: self.renderer.render_layer(lambda x, y: self.tilemap.sample(x, y, dt), parallax=1.0))

        # entity layer
        def draw_entities():
            for entity in world.all_entities():
                pos = entity.get_component(Position)
                glyph = entity.get_component(GlyphComponent)
                if pos and glyph:
                    sx, sy = cam.world_to_screen(pos.x, pos.y)
                    self.renderer.draw_point(sx, sy, glyph.glyph)

        self.pipeline.add_layer(draw_entities)

        # finalize screen
        self.pipeline.add_post(self.renderer.present)

        self.pipeline.run()
