try:
    from numba import cuda
except Exception:
    cuda = None


class RegionGPUContext:
    """
    Assigns CUDA streams per region for potential parallel execution.
    """

    def __init__(self):
        self.streams = {}

    def assign_stream(self, region):
        if cuda is None:
            region.cuda_stream = None
            return
        stream = cuda.stream()
        self.streams[region.region_id] = stream
        region.cuda_stream = stream

    def wait_all(self):
        for stream in self.streams.values():
            stream.synchronize()
