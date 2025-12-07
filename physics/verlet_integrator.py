class VerletIntegrator:
    """
    Position-Verlet integration for stable physics simulation.
    """

    def __init__(self, position=0.0, velocity=0.0):
        self.position = position
        self.velocity = velocity
        self.prev_position = None

    def step(self, force, dt):
        if self.prev_position is None:
            # Bootstrap using velocity
            self.prev_position = self.position - self.velocity * dt

        next_position = 2*self.position - self.prev_position + force*(dt*dt)
        self.velocity = (next_position - self.prev_position) / (2*dt)
        self.prev_position = self.position
        self.position = next_position
