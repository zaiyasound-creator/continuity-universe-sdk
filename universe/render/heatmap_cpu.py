import numpy as np
from universe.render.colormap import cosmic_map


class HeatmapCPU:
    """CPU heatmap renderer using the cosmic colormap."""

    def __init__(self):
        pass

    def render(self, field: np.ndarray) -> np.ndarray:
        fmin, fmax = field.min(), field.max()
        if fmax == fmin:
            normalized = np.zeros_like(field)
        else:
            normalized = (field - fmin) / (fmax - fmin)
        return (cosmic_map(normalized) * 255).astype(np.uint8)
