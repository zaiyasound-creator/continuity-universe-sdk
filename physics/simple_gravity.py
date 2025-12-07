class SimpleGravityField:
    def __init__(self, mass=1.0, gravity=-9.8):
        self.mass = mass
        self.gravity = gravity
        self.position = 0.0
        self.velocity = 0.0
        self.universe = None

    def bind_universe(self, universe):
        self.universe = universe

    def step(self, dt):
        self.velocity += self.gravity * dt
        self.position += self.velocity * dt
