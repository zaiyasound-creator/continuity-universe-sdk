import numpy as np


def cosmic_map(values: np.ndarray) -> np.ndarray:
    """
    Cosine/sine-inspired map producing vibrant cosmic colors for normalized [0,1] inputs.
    """
    r = np.clip(np.sin(values * 6.28) * 0.5 + 0.5, 0, 1)
    g = np.clip(values ** 0.5, 0, 1)
    b = np.clip(1 - values, 0, 1)
    return np.stack([r, g, b], axis=-1)
