from universe.physics.aetherion.field_base import AetherField


class SigmaField(AetherField):
    """
    Coherence density field.
    """

    def __init__(self, width: int = 512, height: int = 512, solver=None):
        super().__init__(width, height)
        self.solver = solver

    def step_cpu(self, dt: float):
        if self.solver is None:
            return
        self.field = self.solver.step(self.field, dt)

    def step_gpu(self, dt: float):
        if self.solver is None:
            return
        # GPU solver returns device array; bring back to host
        self.field = self.solver.step(self.field, dt).copy_to_host()
