from numba import cuda
import math


@cuda.jit
def apply_forces(px, py, fx, fy, n):
    """
    Example global attraction force toward origin; extend as needed for fields/springs.
    """
    i = cuda.grid(1)
    if i >= n:
        return

    cx, cy = 0.0, 0.0
    k = 5.0

    dx = cx - px[i]
    dy = cy - py[i]
    dist = math.sqrt(dx * dx + dy * dy) + 1e-6

    # inverse-square attraction
    f = k / (dist * dist)

    fx[i] += dx * f
    fy[i] += dy * f
