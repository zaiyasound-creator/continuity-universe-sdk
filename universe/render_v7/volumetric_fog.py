import numpy as np
from scipy.ndimage import gaussian_filter


class VolumetricFog:
    """
    Fog density driven by Ache with glow from Sigma.
    """

    def __init__(self, fog_scale: float = 2.0, glow_scale: float = 1.4):
        self.fog_scale = fog_scale
        self.glow_scale = glow_scale

    def apply(self, sigma: np.ndarray, ache: np.ndarray) -> np.ndarray:
        density = gaussian_filter(ache, 2) * self.fog_scale
        glow = gaussian_filter(sigma, 4) * self.glow_scale
        fog = np.clip(density + glow, 0, 255).astype(np.uint8)
        return np.stack([fog, fog, fog], axis=-1)
