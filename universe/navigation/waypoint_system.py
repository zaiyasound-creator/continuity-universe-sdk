from universe.components.position import Position
from universe.components.velocity import Velocity
from universe.navigation.waypoint_graph import WaypointGraph
from universe.systems.base_system import System


class WaypointSystem(System):
    """
    Moves entities toward assigned waypoint nodes.
    """

    def __init__(self, graph: WaypointGraph, name: str = "waypoints", order: int = 19, phase: str = "physics"):
        super().__init__(name=name, order=order, phase=phase)
        self.graph = graph
        self.targets = {}  # entity_id -> node_id

    def set_target(self, entity_id, node_id):
        self.targets[entity_id] = node_id

    def update(self, world, dt: float):
        for eid, node_id in list(self.targets.items()):
            entity = world.get_entity(eid)
            if entity is None:
                self.targets.pop(eid, None)
                continue

            pos = entity.get_component(Position)
            vel = entity.get_component(Velocity)
            if not pos or not vel:
                continue

            if node_id not in self.graph.nodes:
                continue

            tx, ty = self.graph.nodes[node_id]
            dx = tx - pos.x
            dy = ty - pos.y

            vel.vx = dx * dt * 3
            vel.vy = dy * dt * 3
