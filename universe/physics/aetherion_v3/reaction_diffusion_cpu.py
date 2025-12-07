import numpy as np


class ReactionDiffusionCPU:
    """
    Reaction–diffusion solver (Gray-Scott style) for Aetherion Physics v3.
    Governs emergent structures in sigma (U) and Ache (V).
    """

    def __init__(self, Du: float = 0.2, Dv: float = 0.1, F: float = 0.04, k: float = 0.06):
        self.Du = Du  # diffusion of U (sigma)
        self.Dv = Dv  # diffusion of V (Ache)
        self.F = F  # feed rate
        self.k = k  # kill rate

    @staticmethod
    def laplacian(M: np.ndarray) -> np.ndarray:
        return (
            np.roll(M, 1, axis=0)
            + np.roll(M, -1, axis=0)
            + np.roll(M, 1, axis=1)
            + np.roll(M, -1, axis=1)
            - 4 * M
        )

    def step(self, U: np.ndarray, V: np.ndarray, dt: float):
        lapU = self.laplacian(U)
        lapV = self.laplacian(V)

        reaction = U * (V * V)

        dU = self.Du * lapU - reaction + self.F * (1 - U)
        dV = self.Dv * lapV + reaction - (self.F + self.k) * V

        U_new = U + dU * dt
        V_new = V + dV * dt

        return U_new, V_new
