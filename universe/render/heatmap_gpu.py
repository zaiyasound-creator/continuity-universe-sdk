try:
    from numba import cuda
except Exception:  # pragma: no cover
    cuda = None
import numpy as np
from universe.render.colormap import cosmic_map
from universe.render.heatmap_cpu import HeatmapCPU


if cuda:

    @cuda.jit
    def normalize_kernel(field, out, fmin, fmax, w, h):
        x, y = cuda.grid(2)
        if x >= w or y >= h:
            return
        v = field[y, x]
        if fmax > fmin:
            nv = (v - fmin) / (fmax - fmin)
        else:
            nv = 0.0
        out[y, x] = nv


class HeatmapGPU:
    """
    GPU heatmap renderer with CPU fallback when CUDA is unavailable.
    """

    def __init__(self, cpu_fallback=None):
        self.gpu_enabled = cuda is not None
        self.cpu_fallback = cpu_fallback or HeatmapCPU()

    def render(self, field: np.ndarray) -> np.ndarray:
        if not self.gpu_enabled:
            return self.cpu_fallback.render(field)

        h, w = field.shape
        d_field = cuda.to_device(field)
        d_norm = cuda.device_array_like(field)

        threads = (16, 16)
        blocks = ((w + 15) // 16, (h + 15) // 16)

        normalize_kernel[blocks, threads](d_field, d_norm, field.min(), field.max(), w, h)

        cuda.synchronize()
        normalized = d_norm.copy_to_host()
        return (cosmic_map(normalized) * 255).astype(np.uint8)
