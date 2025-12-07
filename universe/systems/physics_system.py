from universe.components.mass import Mass
from universe.components.velocity import Velocity
from universe.systems.base_system import System


class PhysicsSystem(System):
    """
    Applies a simple gravity force to velocity.
    """

    def __init__(self, gravity=(0.0, -9.8, 0.0), name: str = "physics", order: int = 5, phase: str = "physics"):
        super().__init__(name=name, order=order, phase=phase)
        self.gravity = gravity

    def update(self, world, dt: float):
        gx, gy, gz = self.gravity
        for entity in world.all_entities():
            vel = entity.get_component(Velocity)
            mass = entity.get_component(Mass)
            if vel and mass:
                vel.vx += gx * dt
                vel.vy += gy * dt
                vel.vz += gz * dt
