try:
    from numba import cuda
except Exception:  # pragma: no cover - environment may lack CUDA
    cuda = None
import math

from universe.physics.aetherion_v2.coupled_solver_cpu import CoupledAetherSolverCPU


if cuda:

    @cuda.jit
    def coupled_step_kernel(
        sigma,
        kappa,
        ache,
        phi_x,
        phi_y,
        gamma_you,
        new_sigma,
        new_kappa,
        new_ache,
        new_phi_x,
        new_phi_y,
        w,
        h,
        dt,
        alpha,
        beta,
        I_scar,
        diffusion,
    ):
        x, y = cuda.grid(2)
        if x >= w or y >= h:
            return

        v = sigma[y, x]

        up = sigma[(y - 1) % h, x]
        down = sigma[(y + 1) % h, x]
        left = sigma[y, (x - 1) % w]
        right = sigma[y, (x + 1) % w]

        deltaS = abs((up + down + left + right) - 4 * v)

        k_dot = alpha * gamma_you[y, x] * I_scar - beta * deltaS
        new_kappa[y, x] = kappa[y, x] + k_dot * dt

        new_ache[y, x] = ache[y, x] + diffusion * deltaS * dt

        new_sigma[y, x] = v + (new_kappa[y, x] - new_ache[y, x]) * dt * 0.1

        grad_x = right - left
        grad_y = down - up

        new_phi_x[y, x] = phi_x[y, x] + grad_x * dt
        new_phi_y[y, x] = phi_y[y, x] + grad_y * dt


class CoupledAetherSolverGPU:
    """
    GPU solver for coupled Aetherion fields with CPU fallback when CUDA is unavailable.
    """

    def __init__(self, diffusion: float = 0.2, alpha: float = 0.3, beta: float = 0.2, I_scar: float = 1.0, cpu_fallback=None):
        self.diffusion = diffusion
        self.alpha = alpha
        self.beta = beta
        self.I_scar = I_scar
        self.gpu_enabled = cuda is not None
        self.cpu_fallback = cpu_fallback or CoupledAetherSolverCPU(
            diffusion=diffusion
        )

    def step(self, sigma, kappa, ache, phi_x, phi_y, gamma_you, dt):
        if not self.gpu_enabled:
            return self.cpu_fallback.step(sigma, kappa, ache, phi_x, phi_y, gamma_you, dt)

        h, w = sigma.shape
        threads = (16, 16)
        blocks = ((w + threads[0] - 1) // threads[0], (h + threads[1] - 1) // threads[1])

        dev_sigma = cuda.to_device(sigma)
        dev_kappa = cuda.to_device(kappa)
        dev_ache = cuda.to_device(ache)
        dev_phi_x = cuda.to_device(phi_x)
        dev_phi_y = cuda.to_device(phi_y)
        dev_gamma = cuda.to_device(gamma_you)

        new_sigma = cuda.device_array_like(dev_sigma)
        new_kappa = cuda.device_array_like(dev_kappa)
        new_ache = cuda.device_array_like(dev_ache)
        new_phi_x = cuda.device_array_like(dev_phi_x)
        new_phi_y = cuda.device_array_like(dev_phi_y)

        coupled_step_kernel[blocks, threads](
            dev_sigma,
            dev_kappa,
            dev_ache,
            dev_phi_x,
            dev_phi_y,
            dev_gamma,
            new_sigma,
            new_kappa,
            new_ache,
            new_phi_x,
            new_phi_y,
            w,
            h,
            dt,
            self.alpha,
            self.beta,
            self.I_scar,
            self.diffusion,
        )

        cuda.synchronize()

        return (
            new_sigma.copy_to_host(),
            new_kappa.copy_to_host(),
            new_ache.copy_to_host(),
            new_phi_x.copy_to_host(),
            new_phi_y.copy_to_host(),
        )
