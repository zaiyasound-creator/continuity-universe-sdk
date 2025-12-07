from universe.physics.aetherion.field_base import AetherField


class AcheField(AetherField):
    """
    Entropic pressure / strain field.
    """

    def __init__(self, width: int = 512, height: int = 512, solver=None):
        super().__init__(width, height)
        self.solver = solver

    def step_cpu(self, dt: float):
        if self.solver is None:
            return
        self.field = self.solver.step(self.field, dt)

    def step_gpu(self, dt: float):
        self.step_cpu(dt)
