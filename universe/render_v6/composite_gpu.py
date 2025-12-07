try:
    from numba import cuda
except Exception:  # pragma: no cover
    cuda = None

from universe.render.composite_cpu import CompositeCPU


if cuda:

    @cuda.jit
    def composite_kernel(base, overlay, out, alpha):
        x, y = cuda.grid(2)
        if x >= base.shape[1] or y >= base.shape[0]:
            return
        for c in range(3):
            out[y, x, c] = int(base[y, x, c] * alpha + overlay[y, x, c] * (1 - alpha))


class CompositeGPU:
    """
    GPU compositor with CPU fallback.
    """

    def __init__(self, alpha: float = 0.5, cpu_fallback=None):
        self.alpha = alpha
        self.gpu_enabled = cuda is not None
        self.cpu_fallback = cpu_fallback or CompositeCPU(alpha=alpha)

    def composite(self, base, overlay):
        if not self.gpu_enabled:
            return self.cpu_fallback.composite(base, overlay)

        h, w, _ = base.shape
        d_base = cuda.to_device(base)
        d_overlay = cuda.to_device(overlay)
        d_out = cuda.device_array_like(base)

        threads = (16, 16)
        blocks = ((w + 15) // 16, (h + 15) // 16)

        composite_kernel[blocks, threads](d_base, d_overlay, d_out, self.alpha)
        cuda.synchronize()
        return d_out.copy_to_host()
