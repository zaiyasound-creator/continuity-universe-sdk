from universe.physics.aetherion_v3.reaction_diffusion_cpu import ReactionDiffusionCPU
from universe.physics.aetherion_v3.turbulence_cpu import TurbulenceCPU
from universe.physics.aetherion_v2.energy_model import AetherEnergyModel


class AetherionNonlinearSolver:
    """
    Full non-linear coupled solver for Aetherion v3.
    σ, κ, Ache, ϕ⃗ update together with reaction–diffusion, turbulence, and κ̇ law.
    """

    def __init__(self, rd_solver=None, turb_solver=None, energy_model=None):
        self.rd = rd_solver or ReactionDiffusionCPU()
        self.turb = turb_solver or TurbulenceCPU()
        self.energy = energy_model or AetherEnergyModel()

    def step(self, sigma, kappa, ache, phi_x, phi_y, gamma_you, dt: float):
        # Reaction–diffusion on σ (U) and Ache (V)
        sigma, ache = self.rd.step(sigma, ache, dt)

        # Entropy + κ̇ law
        deltaS = self.energy.entropy(sigma)
        k_dot = self.energy.kappa_dot(gamma_you, deltaS)
        kappa = kappa + k_dot * dt

        # Turbulence on flow
        phi_x, phi_y = self.turb.step(phi_x, phi_y, dt)

        # Coupling adjustments
        sigma += 0.05 * kappa * dt
        kappa -= 0.02 * ache * dt

        return sigma, kappa, ache, phi_x, phi_y
