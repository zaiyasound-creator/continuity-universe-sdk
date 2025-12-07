class CollisionSolver:
    """Impulse-based rigid body collision solver."""

    @staticmethod
    def resolve(rb1, rb2, nx: float, ny: float) -> None:
        # relative velocity
        rvx = rb2.vx - rb1.vx
        rvy = rb2.vy - rb1.vy

        vel_along_normal = rvx * nx + rvy * ny
        if vel_along_normal > 0:
            return  # bodies are separating

        restitution = min(rb1.restitution, rb2.restitution)

        # impulse scalar
        j = -(1 + restitution) * vel_along_normal
        j /= rb1.inv_mass + rb2.inv_mass

        impulse_x = j * nx
        impulse_y = j * ny

        # apply impulses
        rb1.vx -= impulse_x * rb1.inv_mass
        rb1.vy -= impulse_y * rb1.inv_mass

        rb2.vx += impulse_x * rb2.inv_mass
        rb2.vy += impulse_y * rb2.inv_mass
