from universe.components.position import Position

try:
    from universe.gpu.gpu_memory import GPUMemory
    from universe.gpu.gpu_scheduler_v8 import GPUSchedulerV8
except Exception:
    GPUMemory = None
    GPUSchedulerV8 = None


class RegionState:
    """
    Holds a regional subset of entities and its own GPU scheduler/buffers.
    """

    def __init__(self, region_id, bounds, max_entities: int = 5000):
        """
        bounds: (x0, y0, x1, y1)
        """
        self.region_id = region_id
        self.bounds = bounds
        self.entities = {}
        self.cuda_stream = None

        self._gpu_available = GPUMemory is not None and GPUSchedulerV8 is not None
        if self._gpu_available:
            self.gpu = GPUMemory(max_entities)
            self.scheduler = GPUSchedulerV8(self.gpu)
        else:
            self.gpu = None
            self.scheduler = None

    def step(self, dt: float, stream=None):
        if self._gpu_available and self.gpu and self.scheduler:
            self.gpu.upload(self.entities)
            self.scheduler.step(dt, stream=stream)
            self._sync_back()
        else:
            # CPU fallback: simple integration
            for ent in self.entities.values():
                pos = ent.get("Position")
                vel = ent.get("Velocity")
                if pos and vel:
                    pos.x += vel.vx * dt
                    pos.y += vel.vy * dt

    def _sync_back(self):
        px = self.gpu.pos_x.copy_to_host()
        py = self.gpu.pos_y.copy_to_host()
        for i, (_, ent) in enumerate(self.entities.items()):
            pos = ent.get("Position")
            if pos:
                pos.x = float(px[i])
                pos.y = float(py[i])
