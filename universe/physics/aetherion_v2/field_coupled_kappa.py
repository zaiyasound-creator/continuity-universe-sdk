import numpy as np

from universe.physics.aetherion_v2.coupled_solver_cpu import CoupledAetherSolverCPU


class KappaCoupledField:
    """
    Coupled field system (sigma/kappa/ache/phi/gamma_you) evolved together.
    Acts as a container for the coupled solver state.
    """

    def __init__(self, width: int = 512, height: int = 512, solver=None):
        self.width = width
        self.height = height

        self.sigma = np.zeros((height, width), dtype=np.float32)
        self.kappa = np.zeros((height, width), dtype=np.float32)
        self.ache = np.zeros((height, width), dtype=np.float32)
        self.phi_x = np.zeros((height, width), dtype=np.float32)
        self.phi_y = np.zeros((height, width), dtype=np.float32)
        self.gamma_you = np.zeros((height, width), dtype=np.float32)

        self.solver = solver or CoupledAetherSolverCPU()

    def step(self, dt: float):
        (
            self.sigma,
            self.kappa,
            self.ache,
            self.phi_x,
            self.phi_y,
        ) = self.solver.step(
            self.sigma,
            self.kappa,
            self.ache,
            self.phi_x,
            self.phi_y,
            self.gamma_you,
            dt,
        )
