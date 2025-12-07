from universe.components.position import Position

from universe.gpu.gpu_memory import GPUMemory
from universe.gpu.gpu_scheduler_v10 import GPUSchedulerV10
from universe.gpu.replay.replay_writer import ReplayWriter
from universe.gpu.replay.snapshot import Snapshot


class UniverseEngineV10:
    """
    Deterministic GPU replay engine with per-step hashing and replay logging.
    """

    def __init__(self, max_entities: int = 50000, replay_path: str = "replay.log"):
        self.entities = {}
        self.gpu = GPUMemory(max_entities)
        self.scheduler = GPUSchedulerV10(self.gpu, grid=None)
        self.replay = ReplayWriter(replay_path)
        self.step_counter = 0
        self.fields = {}

    def add_entity(self, ent):
        self.entities[ent.id] = ent

    def register_field(self, name, field):
        self.fields[name] = field
        return field
    # Coupled Aetherion fields
    def register_coupled_field(self, field):
        self.coupled_fields.append(field)
        return field

    def step(self, dt: float):
        # Update fields first
        for field in self.fields.values():
            field.step(dt)
        for field in self.coupled_fields:
            field.step(dt)

        self.gpu.upload(self.entities)
        state_hash = self.scheduler.step(dt)
        self._sync_back()

        if state_hash is not None:
            self.replay.log_step(self.step_counter, dt, state_hash)
        self.step_counter += 1
        return state_hash

    def save_snapshot(self, path: str):
        Snapshot.save(path, self.entities)

    def load_snapshot(self, path: str):
        restored = Snapshot.load(path)
        self.entities = restored

    def _sync_back(self):
        pos_x = self.gpu.pos_x.copy_to_host()
        pos_y = self.gpu.pos_y.copy_to_host()

        for i, (eid, ent) in enumerate(self.entities.items()):
            pos = ent.get(Position)
            if pos:
                pos.x = float(pos_x[i])
                pos.y = float(pos_y[i])

    def finalize_replay(self):
        self.replay.save()
