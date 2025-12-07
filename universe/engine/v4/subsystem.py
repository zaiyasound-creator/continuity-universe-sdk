class Subsystem:
    """Base class for Universe Engine v4 subsystems."""

    priority = 50  # lower runs earlier

    def __init__(self, universe):
        self.universe = universe

    def fixed_update(self, dt: float):
        """
        Called at fixed time steps (e.g., physics).
        """
        return None

    def update(self, dt: float):
        """
        Called once per variable frame.
        """
        return None
