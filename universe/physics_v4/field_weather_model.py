from universe.physics_v4.aether_storms import AetherStorms
from universe.physics_v4.pressure_fronts import PressureFronts
from universe.physics_v4.thermal_winds import ThermalWinds
from universe.physics_v4.turbulence_driver import TurbulenceDriver


class FieldWeatherModel:
    """
    Combines thermal winds, pressure fronts, storms, and turbulence to evolve flow fields.
    """

    def __init__(self):
        self.thermal = ThermalWinds()
        self.pressure = PressureFronts()
        self.storms = AetherStorms()
        self.turb = TurbulenceDriver()

    def update(self, sigma, ache, kappa, phi_x, phi_y):
        twx, twy = self.thermal.compute(sigma)
        px, py = self.pressure.compute(ache)

        phi_x[:] = twx + px
        phi_y[:] = twy + py

        self.turb.apply(phi_x, phi_y)
        self.storms.apply(sigma, ache, kappa)

        return phi_x, phi_y
