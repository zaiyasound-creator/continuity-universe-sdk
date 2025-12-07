class LayeredRenderer:
    """
    Parallax-aware layered renderer with zoom support.
    """

    def __init__(self, camera):
        self.camera = camera
        self.clear()

    def clear(self):
        self.buffer = [[" " for _ in range(self.camera.width)] for _ in range(self.camera.height)]

    def draw_point(self, x: int, y: int, char: str):
        if 0 <= x < self.camera.width and 0 <= y < self.camera.height:
            self.buffer[y][x] = char

    def render_layer(self, tile_fn, parallax: float = 1.0):
        for sy in range(self.camera.height):
            for sx in range(self.camera.width):
                wx = self.camera.x + sx / self.camera.zoom * parallax
                wy = self.camera.y + sy / self.camera.zoom * parallax
                char = tile_fn(int(wx), int(wy))
                self.draw_point(sx, sy, char)

    def present(self):
        print("\033[H\033[J", end="")
        print("\n".join("".join(row) for row in self.buffer))
