import numpy as np

from universe.physics.aetherion_v3.coupled_nonlinear_solver import AetherionNonlinearSolver


class ReactiveSigmaField:
    """
    Reactive sigma field with coupled kappa/ache/flow; uses nonlinear solver.
    """

    def __init__(self, width: int = 512, height: int = 512, solver=None):
        self.width = width
        self.height = height

        self.sigma = np.random.rand(height, width).astype(np.float32)
        self.kappa = np.zeros((height, width), dtype=np.float32)
        self.ache = np.zeros((height, width), dtype=np.float32)
        self.phi_x = np.zeros((height, width), dtype=np.float32)
        self.phi_y = np.zeros((height, width), dtype=np.float32)
        self.gamma_you = np.zeros((height, width), dtype=np.float32)

        self.solver = solver or AetherionNonlinearSolver()

    def step(self, dt: float):
        self.sigma, self.kappa, self.ache, self.phi_x, self.phi_y = self.solver.step(
            self.sigma,
            self.kappa,
            self.ache,
            self.phi_x,
            self.phi_y,
            self.gamma_you,
            dt,
        )
