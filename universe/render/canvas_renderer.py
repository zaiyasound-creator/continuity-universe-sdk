class CanvasRenderer:
    """
    Grid renderer that maps entities to cells using glyph and position components.
    """

    def __init__(self, width: int = 80, height: int = 40):
        self.width = width
        self.height = height

    def render_entities(self, universe, components):
        grid = [[" " for _ in range(self.width)] for _ in range(self.height)]
        cm = components

        for entity in universe.all_entities():
            pos = entity.get_component(getattr(cm, "Position", None))
            glyph = entity.get_component(getattr(cm, "GlyphComponent", None))

            if pos and glyph:
                x = int(pos.x)
                y = int(pos.y)
                if 0 <= x < self.width and 0 <= y < self.height:
                    grid[y][x] = glyph.glyph

        print("\n".join("".join(row) for row in grid))
