import math

from universe.components.position import Position
from universe.physics.collision_solver import CollisionSolver
from universe.physics.collider import AABBCollider, CircleCollider
from universe.physics.rigidbody import RigidBody


class PhysicsWorld:
    """
    Manages rigid bodies, integrates motion, and resolves collisions.
    """

    def __init__(self):
        self.entities = []

    def add_entity(self, entity) -> None:
        if entity not in self.entities:
            self.entities.append(entity)

    def step(self, dt: float) -> None:
        # Integrate forces -> velocities -> positions
        for ent in self.entities:
            rb = ent.get_component(RigidBody)
            pos = ent.get_component(Position)
            if not rb or not pos:
                continue

            rb.vx += rb.ax * dt
            rb.vy += rb.ay * dt
            rb.ax = rb.ay = 0.0

            pos.x += rb.vx * dt
            pos.y += rb.vy * dt

        # Detect + resolve
        n = len(self.entities)
        for i in range(n):
            for j in range(i + 1, n):
                e1 = self.entities[i]
                e2 = self.entities[j]
                rb1, rb2 = e1.get_component(RigidBody), e2.get_component(RigidBody)
                pos1, pos2 = e1.get_component(Position), e2.get_component(Position)
                col1 = getattr(e1, "collider", None)
                col2 = getattr(e2, "collider", None)
                if not (rb1 and rb2 and pos1 and pos2 and col1 and col2):
                    continue

                # AABB vs AABB
                if isinstance(col1, AABBCollider) and isinstance(col2, AABBCollider):
                    nx, ny = self._aabb_normal(pos1, col1, pos2, col2)
                    if nx or ny:
                        CollisionSolver.resolve(rb1, rb2, nx, ny)

                # Circle vs Circle
                elif isinstance(col1, CircleCollider) and isinstance(col2, CircleCollider):
                    nx, ny = self._circle_normal(pos1, col1, pos2, col2)
                    if nx or ny:
                        CollisionSolver.resolve(rb1, rb2, nx, ny)

    @staticmethod
    def _aabb_normal(p1, c1, p2, c2):
        dx = p2.x - p1.x
        dy = p2.y - p1.y

        overlap_x = (c1.w + c2.w) / 2 - abs(dx)
        overlap_y = (c1.h + c2.h) / 2 - abs(dy)

        if overlap_x > 0 and overlap_y > 0:
            if overlap_x < overlap_y:
                return (1, 0) if dx > 0 else (-1, 0)
            return (0, 1) if dy > 0 else (0, -1)
        return (0, 0)

    @staticmethod
    def _circle_normal(p1, c1, p2, c2):
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        dist = math.sqrt(dx * dx + dy * dy)
        rad = c1.r + c2.r
        if dist < rad and dist > 0:
            return (dx / dist, dy / dist)
        return (0, 0)
