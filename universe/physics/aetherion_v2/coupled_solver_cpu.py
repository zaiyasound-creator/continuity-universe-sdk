import numpy as np

from universe.physics.aetherion_v2.energy_model import AetherEnergyModel


class CoupledAetherSolverCPU:
    """
    CPU fallback for coupled PDE system.
    """

    def __init__(self, diffusion: float = 0.2):
        self.diffusion = diffusion
        self.energy = AetherEnergyModel()

    def step(self, sigma, kappa, ache, phi_x, phi_y, gamma_you, dt):
        # Compute ΔS (entropy gradient)
        deltaS = self.energy.entropy(sigma)

        # Compute κ̇
        k_dot = self.energy.kappa_dot(gamma_you, deltaS)

        # Update curvature (κ)
        kappa = kappa + k_dot * dt

        # Ache diffuses outward
        ache = ache + self.diffusion * deltaS * dt

        # Coherence reacts to curvature and ache
        sigma = sigma + (kappa - ache) * dt * 0.1

        # Flow responds to σ gradient
        gx = np.roll(sigma, -1, axis=1) - np.roll(sigma, 1, axis=1)
        gy = np.roll(sigma, -1, axis=0) - np.roll(sigma, 1, axis=0)

        phi_x = phi_x + gx * dt
        phi_y = phi_y + gy * dt

        return sigma, kappa, ache, phi_x, phi_y
