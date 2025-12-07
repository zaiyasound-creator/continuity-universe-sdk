from universe.components.position import Position
from universe.components.velocity import Velocity
from universe.systems.base_system import System


class MovementSystem(System):
    """
    Integrates position using velocity.
    """

    def __init__(self, name: str = "movement", order: int = 10, phase: str = "physics"):
        super().__init__(name=name, order=order, phase=phase)

    def update(self, world, dt: float):
        for entity in world.all_entities():
            pos = entity.get_component(Position)
            vel = entity.get_component(Velocity)
            if pos and vel:
                pos.x += vel.vx * dt
                pos.y += vel.vy * dt
                pos.z += vel.vz * dt
