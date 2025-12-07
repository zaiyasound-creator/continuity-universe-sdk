import math

try:
    from numba import cuda
except Exception:  # pragma: no cover - environment may lack CUDA
    cuda = None


if cuda:

    @cuda.jit
    def pde_step_kernel(field, out, width, height, dt, diffusion):
        x, y = cuda.grid(2)
        if x >= width or y >= height:
            return

        v = field[y, x]

        lap = (
            field[y, (x - 1) % width]
            + field[y, (x + 1) % width]
            + field[(y - 1) % height, x]
            + field[(y + 1) % height, x]
            - 4 * v
        )

        out[y, x] = v + diffusion * lap * dt


class AetherGPUSolver:
    """
    GPU diffusion solver using a 4-neighbor Laplacian.
    """

    def __init__(self, diffusion: float = 0.2):
        if cuda is None:
            raise RuntimeError("CUDA/numba is required for AetherGPUSolver")
        self.diffusion = diffusion

    def step(self, field, dt: float):
        h, w = field.shape
        threads = (16, 16)
        blocks = ((w + threads[0] - 1) // threads[0], (h + threads[1] - 1) // threads[1])

        dev_field = cuda.to_device(field)
        out = cuda.device_array_like(field)
        pde_step_kernel[blocks, threads](dev_field, out, w, h, dt, self.diffusion)
        return out
