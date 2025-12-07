try:
    from numba import cuda
    import math
except Exception:  # pragma: no cover
    cuda = None

from universe.render.vector_field_cpu import VectorFieldCPU


if cuda:

    @cuda.jit
    def vector_kernel(vx, vy, out, w, h):
        x, y = cuda.grid(2)
        if x >= w or y >= h:
            return

        vxv = vx[y, x]
        vyv = vy[y, x]

        mag = (vxv * vxv + vyv * vyv) ** 0.5
        angle = math.atan2(vyv, vxv)

        out[y, x, 0] = min(255, int(mag * 255))
        out[y, x, 1] = min(255, int((math.sin(angle) + 1) / 2 * 255))
        out[y, x, 2] = min(255, int((math.cos(angle) + 1) / 2 * 255))


class VectorFieldGPU:
    """
    GPU vector field renderer with CPU fallback when CUDA is unavailable.
    """

    def __init__(self, cpu_fallback=None):
        self.gpu_enabled = cuda is not None
        self.cpu_fallback = cpu_fallback or VectorFieldCPU()

    def render(self, vx, vy):
        if not self.gpu_enabled:
            return self.cpu_fallback.render(vx, vy)

        h, w = vx.shape
        d_vx = cuda.to_device(vx)
        d_vy = cuda.to_device(vy)

        out = cuda.device_array((h, w, 3), dtype=np.uint8)

        threads = (16, 16)
        blocks = ((w + 15) // 16, (h + 15) // 16)

        vector_kernel[blocks, threads](d_vx, d_vy, out, w, h)
        cuda.synchronize()

        return out.copy_to_host()
