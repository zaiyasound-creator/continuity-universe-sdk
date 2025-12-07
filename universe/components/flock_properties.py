class FlockProperties:
    """Boids-like parameters for cohesion/alignment/separation."""

    def __init__(self, cohesion: float = 1.0, separation: float = 1.0, alignment: float = 1.0, radius: float = 5.0):
        self.cohesion = cohesion
        self.separation = separation
        self.alignment = alignment
        self.radius = radius
