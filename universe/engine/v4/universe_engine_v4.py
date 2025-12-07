from universe.engine.v4.event_bus import EventBus
from universe.engine.v4.scheduler import Scheduler
from universe.engine.v4.subsystem import Subsystem


class UniverseEngineV4:
    """
    Next-generation engine with event bus, fixed + variable steps, and ordered subsystems.
    """

    def __init__(self, fixed_dt: float = 0.016):
        self.time = 0.0
        self.bus = EventBus()
        self.scheduler = Scheduler(fixed_dt=fixed_dt)
        self.subsystems = []

    def add_subsystem(self, subsystem: Subsystem):
        self.subsystems.append(subsystem)
        self.subsystems.sort(key=lambda s: getattr(s, "priority", 50))

    def step(self, dt: float):
        """
        Main update loop: runs fixed steps then variable steps.
        """
        self.time += dt

        fixed_count = self.scheduler.tick(dt)

        # Fixed updates (e.g., physics)
        for _ in range(fixed_count):
            for ss in self.subsystems:
                ss.fixed_update(self.scheduler.fixed_dt)

        # Variable updates
        for ss in self.subsystems:
            ss.update(dt)
