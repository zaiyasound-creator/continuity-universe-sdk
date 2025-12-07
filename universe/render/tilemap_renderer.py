from universe.render.animation_player import AnimationPlayer


class TilemapRenderer:
    """
    Tile sampler with optional animation support.
    """

    def __init__(self, tilemap, animations=None):
        self.tilemap = tilemap
        self.animations = animations or {}

    def sample(self, x: int, y: int, dt: float):
        try:
            tile = self.tilemap[y][x]
        except Exception:
            return " "

        anim = self.animations.get(tile)
        if isinstance(anim, AnimationPlayer):
            return anim.sample(dt)
        return tile
