from typing import Dict, List, Tuple

from universe.components.position import Position
from universe.components.velocity import Velocity
from universe.navigation.a_star import AStar
from universe.systems.base_system import System


class PathSystem(System):
    """
    Uses A* to generate paths and drives entities along them.
    """

    def __init__(self, grid_map, name: str = "paths", order: int = 18, phase: str = "physics"):
        super().__init__(name=name, order=order, phase=phase)
        self.grid = grid_map
        self.astar = AStar(grid_map)
        self.paths: Dict[int, List[Tuple[int, int]]] = {}

    def set_path(self, entity_id: int, start: Tuple[int, int], goal: Tuple[int, int]) -> None:
        self.paths[entity_id] = self.astar.search(start, goal)

    def update(self, world, dt: float):
        for eid, path in list(self.paths.items()):
            if not path:
                continue

            entity = world.get_entity(eid)
            if entity is None:
                self.paths.pop(eid, None)
                continue

            pos = entity.get_component(Position)
            vel = entity.get_component(Velocity)
            if not pos or not vel:
                continue

            tx, ty = path[0]
            dx = tx - pos.x
            dy = ty - pos.y
            dist = abs(dx) + abs(dy)

            if dist < 0.1:
                path.pop(0)
                continue

            vel.vx = dx * dt * 4
            vel.vy = dy * dt * 4
