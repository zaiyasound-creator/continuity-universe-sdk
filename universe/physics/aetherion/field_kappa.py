from universe.physics.aetherion.field_base import AetherField


class KappaField(AetherField):
    """
    Curvature field capturing harmonic tension.
    """

    def __init__(self, width: int = 512, height: int = 512, solver=None):
        super().__init__(width, height)
        self.solver = solver

    def step_cpu(self, dt: float):
        if self.solver is None:
            return
        self.field = self.solver.step(self.field, dt)

    def step_gpu(self, dt: float):
        # GPU solver could be added; fall back to CPU for now
        self.step_cpu(dt)
