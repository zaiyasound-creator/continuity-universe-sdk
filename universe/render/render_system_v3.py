from universe.components.glyph_component import GlyphComponent
from universe.components.position import Position
from universe.components.velocity import Velocity
from universe.render.camera_system import CameraSystem
from universe.render.fog import Fog
from universe.render.glow import Glow
from universe.render.lighting import LightingEngine
from universe.render.renderer_v3 import RendererV3
from universe.render.trail_renderer import TrailRenderer
from universe.systems.base_system import System


class RenderSystemV3(System):
    """
    Color-aware renderer with lighting, fog, glow, and trails.
    """

    def __init__(self, universe, tilemap, animations=None, name: str = "render_v3", order: int = 200, phase: str = "glyphs"):
        super().__init__(name=name, order=order, phase=phase)
        self.universe = universe
        self.camera_system = CameraSystem(universe)
        self.lighting = LightingEngine()
        self.fog = Fog()
        self.glow = Glow()
        self.trails = TrailRenderer()
        self.tilemap = tilemap
        self.anim = animations or {}

    def update(self, world, dt: float):
        cam = self.camera_system.camera
        renderer = RendererV3(cam)
        renderer.clear()

        # Render tilemap background
        for sy in range(cam.height):
            for sx in range(cam.width):
                wx = int(cam.x + sx / cam.zoom)
                wy = int(cam.y + sy / cam.zoom)

                tile = self.tilemap.sample(wx, wy, dt)

                brightness, (lr, lg, lb) = self.lighting.sample(wx, wy)
                r, g, b = lr, lg, lb

                distance = ((wx - cam.x) ** 2 + (wy - cam.y) ** 2) ** 0.5
                r, g, b = self.fog.apply(r, g, b, distance)

                renderer.draw(sx, sy, tile, r, g, b)

        # Render entities + trails + glow
        for eid, ent in self.universe.entities._entities.items():
            pos = ent.get_component(Position)
            glyph = ent.get_component(GlyphComponent)
            vel = ent.get_component(Velocity)

            if not pos or not glyph:
                continue

            sx, sy = cam.world_to_screen(pos.x, pos.y)

            glow_color = self.glow.sample(eid)
            if glow_color:
                r, g, b = glow_color
            else:
                r, g, b = 255, 255, 255

            renderer.draw(sx, sy, glyph.glyph, r, g, b)

            if vel:
                self.trails.add_point(eid, pos.x, pos.y)
                for hx, hy in self.trails.get_trail(eid):
                    tsx, tsy = cam.world_to_screen(hx, hy)
                    renderer.draw(tsx, tsy, ".", 100, 120, 255)

        renderer.present()
