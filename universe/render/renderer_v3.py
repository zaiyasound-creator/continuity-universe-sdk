from universe.render.color import Color


class RendererV3:
    """
    Color-capable renderer with per-pixel RGB buffers.
    """

    def __init__(self, camera):
        self.camera = camera
        self.clear()

    def clear(self):
        self.buffer = [[" " for _ in range(self.camera.width)] for _ in range(self.camera.height)]
        self.color_buffer = [[(255, 255, 255) for _ in range(self.camera.width)] for _ in range(self.camera.height)]

    def draw(self, sx: int, sy: int, char: str, r: int, g: int, b: int):
        if 0 <= sx < self.camera.width and 0 <= sy < self.camera.height:
            self.buffer[sy][sx] = char
            self.color_buffer[sy][sx] = (r, g, b)

    def present(self):
        print("\033[H\033[J", end="")
        for y in range(self.camera.height):
            line = ""
            for x in range(self.camera.width):
                char = self.buffer[y][x]
                r, g, b = self.color_buffer[y][x]
                line += Color.wrap(char, r, g, b)
            print(line)
