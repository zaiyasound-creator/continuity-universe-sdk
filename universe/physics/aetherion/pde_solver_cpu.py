import numpy as np


class AetherCPUSolver:
    """
    Simple CPU diffusion step using a 4-neighbor Laplacian.
    """

    def __init__(self, diffusion: float = 0.2):
        self.diffusion = diffusion

    def step(self, field, dt: float):
        h, w = field.shape
        out = np.copy(field)

        for y in range(h):
            for x in range(w):
                v = field[y, x]
                lap = (
                    field[y, (x - 1) % w]
                    + field[y, (x + 1) % w]
                    + field[(y - 1) % h, x]
                    + field[(y + 1) % h, x]
                    - 4 * v
                )
                out[y, x] = v + self.diffusion * lap * dt

        return out
