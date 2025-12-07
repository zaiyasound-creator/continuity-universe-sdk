class Camera:
    """Simple camera with position and zoom."""

    def __init__(self, x: float = 0.0, y: float = 0.0, zoom: float = 1.0, width: int = 80, height: int = 40):
        self.x = x
        self.y = y
        self.zoom = zoom
        self.width = width
        self.height = height

    def move_towards(self, tx: float, ty: float, smooth: float = 0.15) -> None:
        """Smoothly move toward a target position."""
        self.x += (tx - self.x) * smooth
        self.y += (ty - self.y) * smooth

    def world_to_screen(self, wx: float, wy: float):
        """Convert world coordinates to screen coordinates."""
        sx = int((wx - self.x) * self.zoom)
        sy = int((wy - self.y) * self.zoom)
        return sx, sy
