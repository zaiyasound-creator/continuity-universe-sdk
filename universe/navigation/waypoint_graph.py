class WaypointGraph:
    """Simple waypoint graph for navigation."""

    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_node(self, node_id, x: float, y: float):
        self.nodes[node_id] = (x, y)
        self.edges.setdefault(node_id, [])

    def add_edge(self, a, b):
        self.edges.setdefault(a, []).append(b)
        self.edges.setdefault(b, []).append(a)
