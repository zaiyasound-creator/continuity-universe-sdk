class GridMap:
    """2D grid navigation map for A* pathfinding."""

    def __init__(self, width: int, height: int, walkable: bool = True):
        self.width = width
        self.height = height
        self.cells = [[walkable for _ in range(height)] for _ in range(width)]

    def is_walkable(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height and self.cells[x][y]
