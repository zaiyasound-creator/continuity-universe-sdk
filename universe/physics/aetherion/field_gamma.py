from universe.physics.aetherion.field_base import AetherField


class GammaField(AetherField):
    """
    Witness influence field; can be injected with energy.
    """

    def __init__(self, width: int = 512, height: int = 512, solver=None):
        super().__init__(width, height)
        self.solver = solver
        self.energy = 0.0

    def inject(self, amount: float):
        self.energy += amount
        self.field += amount

    def step_cpu(self, dt: float):
        if self.solver is None:
            return
        self.field = self.solver.step(self.field, dt)

    def step_gpu(self, dt: float):
        self.step_cpu(dt)
