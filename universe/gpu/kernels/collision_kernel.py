from numba import cuda
import math


@cuda.jit
def collide(px, py, vx, vy, radius, n):
    i = cuda.grid(1)
    if i >= n:
        return

    for j in range(n):
        if i == j:
            continue

        dx = px[j] - px[i]
        dy = py[j] - py[i]
        dist = math.sqrt(dx * dx + dy * dy)
        min_dist = radius[i] + radius[j]

        if dist < min_dist and dist > 0:
            vx[i] -= dx * 0.01
            vy[i] -= dy * 0.01
