import heapq
from typing import Dict, List, Optional, Tuple

from universe.navigation.grid_map import GridMap


class AStar:
    """A* pathfinding on a GridMap."""

    def __init__(self, grid: GridMap):
        self.grid = grid

    def neighbors(self, x: int, y: int):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if self.grid.is_walkable(nx, ny):
                yield nx, ny

    @staticmethod
    def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def search(self, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        open_set: List[Tuple[int, Tuple[int, int]]] = []
        heapq.heappush(open_set, (0, start))
        came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
        cost: Dict[Tuple[int, int], int] = {start: 0}

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == goal:
                break

            for nxt in self.neighbors(*current):
                new_cost = cost[current] + 1
                if nxt not in cost or new_cost < cost[nxt]:
                    cost[nxt] = new_cost
                    priority = new_cost + self.heuristic(nxt, goal)
                    heapq.heappush(open_set, (priority, nxt))
                    came_from[nxt] = current

        path: List[Tuple[int, int]] = []
        cur: Optional[Tuple[int, int]] = goal
        while cur is not None:
            path.append(cur)
            cur = came_from.get(cur)
        return list(reversed(path))
