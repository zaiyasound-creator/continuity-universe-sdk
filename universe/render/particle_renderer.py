class ParticleRenderer:
    """
    Renders simple particles as dots; hook for more complex effects later.
    """

    def render(self, renderer, particle):
        sx, sy = renderer.camera.world_to_screen(particle.x, particle.y)
        renderer.draw_point(sx, sy, ".")
