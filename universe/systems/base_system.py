class System:
    """
    Base system to operate over entities/components.
    """

    def __init__(self, name: str, order: int = 0, phase: str = "logic"):
        self.name = name
        self.order = order
        self.phase = phase

    def update(self, world, dt: float):
        """
        Override to implement system behavior.
        """
        raise NotImplementedError("System.update must be implemented")
