from numba import cuda
import math


@cuda.jit
def swept_circle(px, py, vx, vy, radius, toi, n):
    """
    Time-of-impact (TOI) estimation for moving circles (continuous collision).
    """
    i = cuda.grid(1)
    if i >= n:
        return

    toi[i] = 1.0  # default: no hit in frame

    for j in range(n):
        if i == j:
            continue

        dx = px[j] - px[i]
        dy = py[j] - py[i]
        dvx = vx[j] - vx[i]
        dvy = vy[j] - vy[i]

        a = dvx * dvx + dvy * dvy
        if a < 1e-6:
            continue

        b = 2 * (dx * dvx + dy * dvy)
        r = radius[i] + radius[j]
        c = dx * dx + dy * dy - r * r

        disc = b * b - 4 * a * c
        if disc < 0:
            continue

        t = (-b - math.sqrt(disc)) / (2 * a)
        if 0 <= t < toi[i]:
            toi[i] = t
