import math

from universe.components.position import Position
from universe.components.steering import Steering
from universe.components.velocity import Velocity
from universe.systems.base_system import System


class SteeringSystem(System):
    """
    Applies steering forces (seek-like) toward targets.
    """

    def __init__(self, name: str = "steering", order: int = 15, phase: str = "physics"):
        super().__init__(name=name, order=order, phase=phase)

    def update(self, world, dt: float):
        for entity in world.all_entities():
            steer = entity.get_component(Steering)
            pos = entity.get_component(Position)
            vel = entity.get_component(Velocity)

            if not (steer and pos and vel and steer.target):
                continue

            tx, ty, tz = steer.target
            dx = tx - pos.x
            dy = ty - pos.y
            dz = tz - pos.z

            dist = math.sqrt(dx * dx + dy * dy + dz * dz)
            if dist == 0:
                continue

            fx = (dx / dist) * steer.max_force
            fy = (dy / dist) * steer.max_force
            fz = (dz / dist) * steer.max_force

            vel.vx += fx * dt
            vel.vy += fy * dt
            vel.vz += fz * dt
