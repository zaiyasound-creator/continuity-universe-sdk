from numba import cuda


@cuda.jit
def integrate(vx, vy, fx, fy, mass, dt, n):
    """
    Velocity integration using accumulated forces (F = m*a).
    """
    i = cuda.grid(1)
    if i < n:
        vx[i] += (fx[i] / mass[i]) * dt
        vy[i] += (fy[i] / mass[i]) * dt
