from universe.physics_v4.field_weather_model import FieldWeatherModel
from universe.physics_v4.update_kernel_cpu import UpdateKernelCPU


class AetherionV4Integration:
    """
    Integration scaffold for weather-driven Aetherion fields.
    Expects engine.main_field to expose sigma, ache, kappa, phi_x, phi_y arrays.
    """

    def __init__(self, engine):
        self.engine = engine
        self.weather = FieldWeatherModel()
        self.kernel = UpdateKernelCPU()

    def step(self, dt: float):
        f = getattr(self.engine, "main_field", None)
        if f is None:
            return

        f.phi_x, f.phi_y = self.weather.update(f.sigma, f.ache, f.kappa, f.phi_x, f.phi_y)
        self.kernel.step(f, dt)
