from numba import cuda

from universe.gpu.kernels.force_kernel import apply_forces
from universe.gpu.kernels.narrowphase_kernel import integrate
from universe.gpu.kernels.swept_collision_kernel import swept_circle
from universe.gpu.kernels.impulse_kernel import apply_impulse
from universe.gpu.kernels.physics_kernel import physics_step


class GPUSchedulerV8:
    """
    Launches v8 physics kernels: forces -> integrate -> swept TOI -> impulse -> final step.
    """

    def __init__(self, gpu_memory):
        self.gpu = gpu_memory
        self.toi = cuda.device_array(self.gpu.max, dtype=self.gpu.pos_x.dtype)

    def step(self, dt: float):
        n = self.gpu.count
        threads = 256
        blocks = (n + threads - 1) // threads

        if n == 0:
            return

        # Force accumulation
        apply_forces[blocks, threads](
            self.gpu.pos_x,
            self.gpu.pos_y,
            self.gpu.force_x,
            self.gpu.force_y,
            n,
        )

        # Integrate velocity using forces
        integrate[blocks, threads](
            self.gpu.vel_x,
            self.gpu.vel_y,
            self.gpu.force_x,
            self.gpu.force_y,
            self.gpu.mass,
            dt,
            n,
        )

        # Swept TOI for continuous collision
        swept_circle[blocks, threads](
            self.gpu.pos_x,
            self.gpu.pos_y,
            self.gpu.vel_x,
            self.gpu.vel_y,
            self.gpu.radius,
            self.toi,
            n,
        )

        # Impulse resolution
        apply_impulse[blocks, threads](
            self.gpu.pos_x,
            self.gpu.pos_y,
            self.gpu.vel_x,
            self.gpu.vel_y,
            self.gpu.radius,
            self.gpu.mass,
            self.toi,
            n,
        )

        # Final positional integration
        physics_step[blocks, threads](
            self.gpu.pos_x,
            self.gpu.pos_y,
            self.gpu.vel_x,
            self.gpu.vel_y,
            dt,
            n,
        )

        cuda.synchronize()
