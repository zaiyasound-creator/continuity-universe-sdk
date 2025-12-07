class RegionManager:
    """
    Spatial partitioning into regions for parallel-friendly processing.
    """

    def __init__(self, world_size: int = 1000, region_size: int = 50):
        self.world_size = world_size
        self.region_size = region_size
        self.regions = {}

    def region_of(self, x: float, y: float):
        rx = int(x // self.region_size)
        ry = int(y // self.region_size)
        return (rx, ry)

    def add_entity(self, entity, pos) -> None:
        r = self.region_of(pos.x, pos.y)
        self.regions.setdefault(r, []).append(entity)
