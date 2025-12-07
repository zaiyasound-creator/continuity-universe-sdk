try:
    from numba import cuda
except Exception:  # pragma: no cover
    cuda = None

import math

from universe.physics.aetherion_v3.reaction_diffusion_cpu import ReactionDiffusionCPU


if cuda:

    @cuda.jit
    def rd_kernel(U, V, Uout, Vout, w, h, dt, Du, Dv, F, k):
        x, y = cuda.grid(2)
        if x >= w or y >= h:
            return

        u = U[y, x]
        v = V[y, x]

        lapU = (
            U[(y - 1) % h, x]
            + U[(y + 1) % h, x]
            + U[y, (x - 1) % w]
            + U[y, (x + 1) % w]
            - 4 * u
        )
        lapV = (
            V[(y - 1) % h, x]
            + V[(y + 1) % h, x]
            + V[y, (x - 1) % w]
            + V[y, (x + 1) % w]
            - 4 * v
        )

        reaction = u * v * v

        Uout[y, x] = u + (Du * lapU - reaction + F * (1 - u)) * dt
        Vout[y, x] = v + (Dv * lapV + reaction - (F + k) * v) * dt


class ReactionDiffusionGPU:
    """
    GPU RD solver with automatic CPU fallback when CUDA is unavailable.
    """

    def __init__(self, Du: float = 0.2, Dv: float = 0.1, F: float = 0.04, k: float = 0.06, cpu_fallback=None):
        self.Du = Du
        self.Dv = Dv
        self.F = F
        self.k = k
        self.gpu_enabled = cuda is not None
        self.cpu_fallback = cpu_fallback or ReactionDiffusionCPU(Du=Du, Dv=Dv, F=F, k=k)

    def step(self, U, V, dt: float):
        if not self.gpu_enabled:
            return self.cpu_fallback.step(U, V, dt)

        h, w = U.shape
        threads = (16, 16)
        blocks = ((w + 15) // 16, (h + 15) // 16)

        Uout = cuda.device_array_like(U)
        Vout = cuda.device_array_like(V)

        rd_kernel[blocks, threads](
            U,
            V,
            Uout,
            Vout,
            w,
            h,
            dt,
            self.Du,
            self.Dv,
            self.F,
            self.k,
        )

        cuda.synchronize()
        return Uout.copy_to_host(), Vout.copy_to_host()
