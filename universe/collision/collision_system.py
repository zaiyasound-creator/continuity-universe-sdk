from universe.collision.aabb_collider import AABBCollider
from universe.collision.collision_events import CollisionEvent, TriggerEvent
from universe.collision.trigger_collider import TriggerCollider
from universe.components.position import Position
from universe.systems.base_system import System


class CollisionSystem(System):
    """
    Broad-phase AABB collision checks and trigger detection.
    Emits events via an optional event_bus if provided at construction.
    """

    def __init__(self, event_bus=None, name: str = "collision", order: int = 12, phase: str = "physics"):
        super().__init__(name=name, order=order, phase=phase)
        self.event_bus = event_bus

    def update(self, world, dt: float):
        colliders = []
        triggers = []

        # Collect colliders/triggers with positions
        for entity in world.all_entities():
            pos = entity.get_component(Position)
            if pos is None:
                continue

            for comp in entity._components.values():
                if isinstance(comp, AABBCollider):
                    colliders.append((entity, pos, comp))
                elif isinstance(comp, TriggerCollider) and getattr(comp, "active", True):
                    triggers.append((entity, pos, comp))

        # Solid collisions
        for i in range(len(colliders)):
            e1, p1, c1 = colliders[i]
            for j in range(i + 1, len(colliders)):
                e2, p2, c2 = colliders[j]
                if self.intersects(p1, c1, p2, c2):
                    self._emit("collision", CollisionEvent(e1, e2))

        # Trigger checks
        for ent, pos, trig in triggers:
            for other, opos, ocoll in colliders:
                if other is ent:
                    continue
                if self.intersects(pos, trig, opos, ocoll):
                    self._emit("trigger", TriggerEvent(ent, other))

    def _emit(self, event_type: str, payload):
        if self.event_bus:
            self.event_bus.publish(event_type, payload)

    @staticmethod
    def intersects(pos1, col1, pos2, col2):
        return (
            abs(pos1.x - pos2.x) * 2 < (col1.w + col2.w)
            and abs(pos1.y - pos2.y) * 2 < (col1.h + col2.h)
        )
