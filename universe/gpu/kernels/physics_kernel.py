from numba import cuda


@cuda.jit
def physics_step(px, py, vx, vy, dt, n):
    i = cuda.grid(1)
    if i < n:
        px[i] += vx[i] * dt
        py[i] += vy[i] * dt
