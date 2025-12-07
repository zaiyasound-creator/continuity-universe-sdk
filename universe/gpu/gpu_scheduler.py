from numba import cuda

from universe.gpu.kernels.collision_kernel import collide
from universe.gpu.kernels.physics_kernel import physics_step
from universe.gpu.kernels.velocity_kernel import velocity_update


class GPUScheduler:
    """
    Launches CUDA kernels in sequence for physics and collision.
    """

    def __init__(self, gpu_memory):
        self.gpu = gpu_memory

    def step(self, dt: float):
        n = self.gpu.count
        threads = 256
        blocks = (n + threads - 1) // threads

        # Motion integration
        physics_step[blocks, threads](
            self.gpu.pos_x,
            self.gpu.pos_y,
            self.gpu.vel_x,
            self.gpu.vel_y,
            dt,
            n,
        )

        # Collision
        collide[blocks, threads](
            self.gpu.pos_x,
            self.gpu.pos_y,
            self.gpu.vel_x,
            self.gpu.vel_y,
            self.gpu.radius,
            n,
        )

        cuda.synchronize()
