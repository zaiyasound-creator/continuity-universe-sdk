from numba import cuda
import math


@cuda.jit
def apply_impulse(px, py, vx, vy, radius, mass, toi, n):
    """
    Resolve collisions at time-of-impact using an elastic impulse model.
    """
    i = cuda.grid(1)
    if i >= n:
        return

    t = toi[i]
    if t >= 1.0:
        return

    # position at time of impact for body i
    px_i = px[i] + vx[i] * t
    py_i = py[i] + vy[i] * t

    for j in range(n):
        if j == i:
            continue

        dx = px[j] - px_i
        dy = py[j] - py_i
        dist = math.sqrt(dx * dx + dy * dy)
        r = radius[i] + radius[j]

        if dist < r and dist > 0:
            nx = dx / dist
            ny = dy / dist

            vi = vx[i] * nx + vy[i] * ny
            vj = vx[j] * nx + vy[j] * ny

            m = mass[i] + mass[j]
            imp = (2 * (vi - vj)) / m

            vx[i] -= imp * mass[j] * nx
            vy[i] -= imp * mass[j] * ny
