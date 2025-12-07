try:
    from numba import cuda
except Exception:  # pragma: no cover
    cuda = None

from universe.physics.aetherion_v3.turbulence_cpu import TurbulenceCPU


if cuda:

    @cuda.jit
    def turb_kernel(vx, vy, vx_out, vy_out, w, h, dt, visc):
        x, y = cuda.grid(2)
        if x >= w or y >= h:
            return

        vorticity = (
            vy[y, (x + 1) % w]
            - vy[y, (x - 1) % w]
            - vx[(y + 1) % h, x]
            + vx[(y - 1) % h, x]
        )

        vx_out[y, x] = vx[y, x] + visc * vorticity * dt
        vy_out[y, x] = vy[y, x] - visc * vorticity * dt


class TurbulenceGPU:
    """
    GPU turbulence solver with automatic CPU fallback when CUDA is unavailable.
    """

    def __init__(self, viscosity: float = 0.001, cpu_fallback=None):
        self.visc = viscosity
        self.gpu_enabled = cuda is not None
        self.cpu_fallback = cpu_fallback or TurbulenceCPU(viscosity=viscosity)

    def step(self, vx, vy, dt: float):
        if not self.gpu_enabled:
            return self.cpu_fallback.step(vx, vy, dt)

        h, w = vx.shape
        threads = (16, 16)
        blocks = ((w + 15) // 16, (h + 15) // 16)

        vx_out = cuda.device_array_like(vx)
        vy_out = cuda.device_array_like(vy)

        turb_kernel[blocks, threads](vx, vy, vx_out, vy_out, w, h, dt, self.visc)

        cuda.synchronize()
        return vx_out.copy_to_host(), vy_out.copy_to_host()
