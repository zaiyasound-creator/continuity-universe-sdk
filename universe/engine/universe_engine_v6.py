try:
    from universe.gpu.gpu_memory import GPUMemory
    from universe.gpu.gpu_scheduler import GPUScheduler
except Exception as exc:  # pragma: no cover - environment may not have CUDA
    GPUMemory = None
    GPUScheduler = None
    _gpu_import_error = exc
else:
    _gpu_import_error = None

from universe.components.position import Position
from universe.components.velocity import Velocity


class UniverseEngineV6:
    """
    CUDA-accelerated engine that packs ECS data into GPU buffers and runs kernels.

    Falls back to CPU integration if CUDA/numba is not available.
    """

    def __init__(self, max_entities: int = 50000):
        self.entities = {}
        self._gpu_available = GPUMemory is not None
        self._gpu_error = _gpu_import_error
        if self._gpu_available:
            self.gpu = GPUMemory(max_entities=max_entities)
            self.scheduler = GPUScheduler(self.gpu)
        else:
            self.gpu = None
            self.scheduler = None

    def add_entity(self, entity):
        self.entities[entity.id] = entity
        return entity

    def step(self, dt: float):
        if self._gpu_available:
            self._step_gpu(dt)
        else:
            self._step_cpu(dt)

    def _step_gpu(self, dt: float):
        # Upload ECS state to GPU
        self.gpu.upload(self.entities)

        # Run GPU kernels
        self.scheduler.step(dt)

        # Sync results back to ECS
        self._sync_back()

    def _step_cpu(self, dt: float):
        """
        Simple CPU fallback: integrate positions using velocity.
        """
        for ent in self.entities.values():
            pos = ent.get_component(Position)
            vel = ent.get_component(Velocity)
            if pos and vel:
                pos.x += vel.vx * dt
                pos.y += vel.vy * dt

    def _sync_back(self):
        px = self.gpu.pos_x.copy_to_host()
        py = self.gpu.pos_y.copy_to_host()
        for i, (eid, ent) in enumerate(self.entities.items()):
            pos = ent.get_component(Position) if hasattr(ent, "get_component") else ent.get("Position")
            if pos:
                pos.x = float(px[i])
                pos.y = float(py[i])
