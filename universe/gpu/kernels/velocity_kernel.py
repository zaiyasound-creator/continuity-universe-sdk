from numba import cuda


@cuda.jit
def velocity_update(vx, vy, ax, ay, dt, n):
    i = cuda.grid(1)
    if i < n:
        vx[i] += ax[i] * dt
        vy[i] += ay[i] * dt
