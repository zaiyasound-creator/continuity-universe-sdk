try:
    from universe.gpu.gpu_memory import GPUMemory
    from universe.gpu.gpu_scheduler import GPUScheduler
except Exception as exc:  # pragma: no cover - environment may not have CUDA
    GPUMemory = None
    GPUScheduler = None
    _gpu_import_error = exc
else:
    _gpu_import_error = None


class UniverseEngineV6:
    """
    CUDA-accelerated engine that packs ECS data into GPU buffers and runs kernels.
    """

    def __init__(self, max_entities: int = 50000):
        if GPUMemory is None:
            raise RuntimeError(f"CUDA/numba not available: {_gpu_import_error}")
        self.entities = {}
        self.gpu = GPUMemory(max_entities=max_entities)
        self.scheduler = GPUScheduler(self.gpu)

    def step(self, dt: float):
        # Upload ECS state to GPU
        self.gpu.upload(self.entities)

        # Run GPU kernels
        self.scheduler.step(dt)

        # Sync results back to ECS
        self._sync_back()

    def _sync_back(self):
        px = self.gpu.pos_x.copy_to_host()
        py = self.gpu.pos_y.copy_to_host()
        for i, (eid, ent) in enumerate(self.entities.items()):
            pos = ent.get_component("Position") if hasattr(ent, "get_component") else ent.get("Position")
            if pos:
                pos.x = float(px[i])
                pos.y = float(py[i])
