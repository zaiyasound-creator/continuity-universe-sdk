from universe.gpu.regions.region_gpu_context import RegionGPUContext
from universe.gpu.regions.region_scheduler import RegionScheduler
from universe.gpu.regions.region_state import RegionState


class UniverseEngineV9:
    """
    Multi-region GPU engine: parallel region simulation with entity migration.
    """

    def __init__(self, world_regions):
        """
        world_regions: dict[(ix, iy)] = (x0, y0, x1, y1)
        """
        self.regions = {}
        for rid, bounds in world_regions.items():
            self.regions[rid] = RegionState(rid, bounds)

        self.gpu_context = RegionGPUContext()
        self.scheduler = RegionScheduler(self.regions, self.gpu_context)

    def step(self, dt: float):
        self.scheduler.step(dt)
