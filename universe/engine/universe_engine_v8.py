from universe.components.position import Position
from universe.components.velocity import Velocity

try:
    from universe.gpu.gpu_memory import GPUMemory
    from universe.gpu.gpu_scheduler_v8 import GPUSchedulerV8
except Exception as exc:  # pragma: no cover
    GPUMemory = None
    GPUSchedulerV8 = None
    _gpu_import_error = exc
else:
    _gpu_import_error = None


class UniverseEngineV8:
    """
    GPU narrowphase physics with forces, swept collision, and impulses.
    Falls back to CPU integration if CUDA is unavailable.
    """

    def __init__(self, max_entities: int = 50000):
        self.entities = {}
        self._gpu_available = GPUMemory is not None
        self._gpu_error = _gpu_import_error
        if self._gpu_available:
            self.gpu = GPUMemory(max_entities=max_entities)
            self.scheduler = GPUSchedulerV8(self.gpu)
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
        if self.gpu is None or self.scheduler is None:
            return self._step_cpu(dt)
        self.gpu.upload(self.entities)
        self.scheduler.step(dt)
        self._sync_back()

    def _step_cpu(self, dt: float):
        for ent in self.entities.values():
            pos = ent.get_component(Position)
            vel = ent.get_component(Velocity)
            if pos and vel:
                pos.x += vel.vx * dt
                pos.y += vel.vy * dt

    def _sync_back(self):
        px = self.gpu.pos_x.copy_to_host()
        py = self.gpu.pos_y.copy_to_host()
        for i, (_, ent) in enumerate(self.entities.items()):
            pos = ent.get_component(Position)
            if pos:
                pos.x = float(px[i])
                pos.y = float(py[i])
