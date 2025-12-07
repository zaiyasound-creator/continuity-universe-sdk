from universe.engine.v4.event_bus import EventBus
from universe.engine.v4.scheduler import Scheduler
from universe.engine.v4.subsystem import Subsystem
from universe.engine.v5.double_buffer import DoubleBuffer
from universe.engine.v5.region_manager import RegionManager
from universe.engine.v5.task_graph import TaskGraph
from universe.engine.v5.thread_pool import ThreadPool


class UniverseEngineV5:
    """
    Multithreaded, async-aware engine with region partitioning and GPU hooks.
    """

    def __init__(self, workers: int = 8):
        self.time = 0.0
        self.bus = EventBus()
        self.scheduler = Scheduler()
        self.thread_pool = ThreadPool(workers)
        self.task_graph = TaskGraph()
        self.region = RegionManager()
        self.buffer = DoubleBuffer()
        self.subsystems = []

    def add_subsystem(self, subsystem: Subsystem):
        self.subsystems.append(subsystem)
        node = self.task_graph.add(subsystem)
        return node

    def step(self, dt: float):
        self.time += dt

        fixed_count = self.scheduler.tick(dt)
        for _ in range(fixed_count):
            self._run_parallel(lambda ss: ss.fixed_update(self.scheduler.fixed_dt))

        self._run_parallel(lambda ss: ss.update(dt))

        self.buffer.swap()

    def _run_parallel(self, fn):
        futures = []
        for ss in self.subsystems:
            futures.append(self.thread_pool.submit(fn, ss))

        for f in futures:
            f.result()
