class ASCIIRenderer:
    """
    Minimal ASCII renderer for debugging and quick visualization.
    """

    def __init__(self, width: int = 80, height: int = 40):
        self.width = width
        self.height = height
        self.clear()

    def clear(self):
        self.buffer = [[" " for _ in range(self.width)] for _ in range(self.height)]

    def draw_point(self, x: int, y: int, char: str = "*"):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.buffer[int(y)][int(x)] = char

    def render(self):
        print("\n".join("".join(row) for row in self.buffer))
