import math

from universe.components.flock_properties import FlockProperties
from universe.components.position import Position
from universe.components.velocity import Velocity
from universe.systems.base_system import System


class FlockingSystem(System):
    """
    Classic boids-inspired cohesion, separation, alignment.
    """

    def __init__(self, name: str = "flocking", order: int = 20, phase: str = "physics"):
        super().__init__(name=name, order=order, phase=phase)

    def update(self, world, dt: float):
        # Pre-collect positions for neighbors
        positions = {e.id: e.get_component(Position) for e in world.all_entities()}

        for entity in world.all_entities():
            flock = entity.get_component(FlockProperties)
            pos = entity.get_component(Position)
            vel = entity.get_component(Velocity)
            if not (flock and pos and vel):
                continue

            coh = [0.0, 0.0, 0.0]
            sep = [0.0, 0.0, 0.0]
            ali = [0.0, 0.0, 0.0]
            count = 0

            for oid, opos in positions.items():
                if oid == entity.id or opos is None:
                    continue

                dx = opos.x - pos.x
                dy = opos.y - pos.y
                dz = opos.z - pos.z
                d = math.sqrt(dx * dx + dy * dy + dz * dz)

                if d < flock.radius and d > 0:
                    coh[0] += opos.x
                    coh[1] += opos.y
                    coh[2] += opos.z

                    sep[0] -= dx / (d + 1e-5)
                    sep[1] -= dy / (d + 1e-5)
                    sep[2] -= dz / (d + 1e-5)

                    neighbor = world.get_entity(oid)
                    nvel = neighbor.get_component(Velocity) if neighbor else None
                    if nvel:
                        ali[0] += nvel.vx
                        ali[1] += nvel.vy
                        ali[2] += nvel.vz

                    count += 1

            if count > 0:
                vel.vx += (coh[0] / count - pos.x) * flock.cohesion * dt
                vel.vy += (coh[1] / count - pos.y) * flock.cohesion * dt
                vel.vz += (coh[2] / count - pos.z) * flock.cohesion * dt

                vel.vx += sep[0] * flock.separation * dt
                vel.vy += sep[1] * flock.separation * dt
                vel.vz += sep[2] * flock.separation * dt

                vel.vx += (ali[0] / count - vel.vx) * flock.alignment * dt
                vel.vy += (ali[1] / count - vel.vy) * flock.alignment * dt
                vel.vz += (ali[2] / count - vel.vz) * flock.alignment * dt
