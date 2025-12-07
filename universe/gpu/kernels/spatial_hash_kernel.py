from numba import cuda


@cuda.jit
def spatial_hash(px, py, hash_out, cell_size, n):
    i = cuda.grid(1)
    if i < n:
        cx = int(px[i] / cell_size)
        cy = int(py[i] / cell_size)
        hash_out[i] = (cx * 73856093) ^ (cy * 19349663)
