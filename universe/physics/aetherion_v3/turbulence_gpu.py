try:
    from numba import cuda
except Exception:  # pragma: no cover
    cuda = None


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
    def __init__(self, viscosity: float = 0.001):
        if cuda is None:
            raise RuntimeError("CUDA/numba is required for TurbulenceGPU")
        self.visc = viscosity

    def step(self, vx, vy, dt: float):
        h, w = vx.shape
        threads = (16, 16)
        blocks = ((w + 15) // 16, (h + 15) // 16)

        vx_out = cuda.device_array_like(vx)
        vy_out = cuda.device_array_like(vy)

        turb_kernel[blocks, threads](vx, vy, vx_out, vy_out, w, h, dt, self.visc)

        cuda.synchronize()
        return vx_out.copy_to_host(), vy_out.copy_to_host()
