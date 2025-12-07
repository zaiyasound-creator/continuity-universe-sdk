from numba import cuda

from universe.gpu.replay.determinism import Determinism
from universe.gpu.replay.rng import DeterministicRNG
from universe.gpu.kernels.physics_kernel import physics_step


class GPUSchedulerV10:
    """
    Deterministic GPU scheduler with step hashing for replay validation.
    """

    def __init__(self, gpu_memory, grid=None, seed: int = 12345):
        self.gpu = gpu_memory
        self.grid = grid
        self.rng = DeterministicRNG(seed=seed)
        self.step_idx = 0

    def step(self, dt: float):
        n = self.gpu.count
        threads = 256
        blocks = (n + threads - 1) // threads

        if n == 0:
            return None

        seed = self.rng.next()  # deterministic seed if needed by kernels
        _ = seed  # placeholder; extend kernels to consume this seed

        physics_step[blocks, threads](
            self.gpu.pos_x,
            self.gpu.pos_y,
            self.gpu.vel_x,
            self.gpu.vel_y,
            dt,
            n,
        )

        cuda.synchronize()

        state_hash = Determinism.hash_state(
            {
                "pos_x": self.gpu.pos_x.copy_to_host(),
                "pos_y": self.gpu.pos_y.copy_to_host(),
                "vel_x": self.gpu.vel_x.copy_to_host(),
                "vel_y": self.gpu.vel_y.copy_to_host(),
            }
        )

        self.step_idx += 1
        return state_hash
