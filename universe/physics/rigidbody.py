class RigidBody:
    """Full rigid-body physics component (2D simplified)."""

    def __init__(self, mass: float = 1.0, restitution: float = 0.5):
        self.mass = mass
        self.inv_mass = 0.0 if mass == 0 else 1.0 / mass
        self.restitution = restitution

        # Linear motion
        self.vx = 0.0
        self.vy = 0.0
        self.ax = 0.0
        self.ay = 0.0

    def apply_force(self, fx: float, fy: float) -> None:
        """Accumulate acceleration from a force."""
        if self.inv_mass == 0:
            return
        self.ax += fx * self.inv_mass
        self.ay += fy * self.inv_mass
