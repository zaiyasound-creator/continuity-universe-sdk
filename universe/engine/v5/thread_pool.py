from concurrent.futures import ThreadPoolExecutor


class ThreadPool:
    """Simple thread pool wrapper."""

    def __init__(self, workers: int = 8):
        self.executor = ThreadPoolExecutor(max_workers=workers)

    def submit(self, fn, *args, **kwargs):
        return self.executor.submit(fn, *args, **kwargs)
