import numpy as np

try:
    from numba import cuda
except ImportError:  # pragma: no cover - environment may not have CUDA
    cuda = None

from universe.components.position import Position
from universe.components.velocity import Velocity


class GPUMemory:
    """
    Manages GPU buffers for SoA component data.

    Uses a fixed maximum entity count; callers should check `count` for active size.
    """

    def __init__(self, max_entities: int = 50000):
        if cuda is None:
            raise RuntimeError("numba.cuda is required for GPUMemory")

        self.max = max_entities

        # Device arrays
        self.pos_x = cuda.device_array(self.max, dtype=np.float32)
        self.pos_y = cuda.device_array(self.max, dtype=np.float32)
        self.vel_x = cuda.device_array(self.max, dtype=np.float32)
        self.vel_y = cuda.device_array(self.max, dtype=np.float32)
        self.radius = cuda.device_array(self.max, dtype=np.float32)
        self.mass = cuda.device_array(self.max, dtype=np.float32)
        self.force_x = cuda.device_array(self.max, dtype=np.float32)
        self.force_y = cuda.device_array(self.max, dtype=np.float32)

        self.count = 0

    def upload(self, entities: dict) -> None:
        """
        Copy ECS state (positions/velocities) into GPU arrays.
        """
        n = min(len(entities), self.max)
        self.count = n

        host_pos_x = np.zeros(self.max, dtype=np.float32)
        host_pos_y = np.zeros(self.max, dtype=np.float32)
        host_vel_x = np.zeros(self.max, dtype=np.float32)
        host_vel_y = np.zeros(self.max, dtype=np.float32)
        host_radius = np.ones(self.max, dtype=np.float32)
        host_mass = np.ones(self.max, dtype=np.float32)

        for i, (_, ent) in enumerate(entities.items()):
            if i >= self.max:
                break
            pos = ent.get_component(Position) if hasattr(ent, "get_component") else ent.get("Position")
            vel = ent.get_component(Velocity) if hasattr(ent, "get_component") else ent.get("Velocity")

            if pos:
                host_pos_x[i] = getattr(pos, "x", 0.0)
                host_pos_y[i] = getattr(pos, "y", 0.0)
            if vel:
                host_vel_x[i] = getattr(vel, "vx", 0.0)
                host_vel_y[i] = getattr(vel, "vy", 0.0)
            host_radius[i] = getattr(ent, "radius", 1.0)
            host_mass[i] = getattr(ent, "mass", 1.0)

        self.pos_x.copy_to_device(host_pos_x)
        self.pos_y.copy_to_device(host_pos_y)
        self.vel_x.copy_to_device(host_vel_x)
        self.vel_y.copy_to_device(host_vel_y)
        self.radius.copy_to_device(host_radius)
        self.mass.copy_to_device(host_mass)
        # Clear forces
        self.force_x.copy_to_device(np.zeros(self.max, dtype=np.float32))
        self.force_y.copy_to_device(np.zeros(self.max, dtype=np.float32))
