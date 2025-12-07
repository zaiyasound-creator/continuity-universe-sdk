import numpy as np

from universe.render_v7.aether_lightning import AetherLightning
from universe.render_v7.aether_rain import AetherRain
from universe.render_v7.curvature_thunder import CurvatureThunder
from universe.render_v7.pressure_fog_wall import PressureFogWall
from universe.render_v7.storm_glow import StormGlow
from universe.render_v7.storm_motion_blur import StormMotionBlur
from universe.render_v7.volumetric_fog import VolumetricFog


class RendererV7:
    """
    Atmospheric/storm visualizer for Aetherion weather fields.
    """

    def __init__(self, width: int, height: int):
        self.w, self.h = width, height

        self.fog = VolumetricFog()
        self.glow = StormGlow()
        self.lightning = AetherLightning()
        self.thunder = CurvatureThunder()
        self.wall = PressureFogWall()
        self.rain = AetherRain()
        self.motion = StormMotionBlur()

    def render(self, sigma: np.ndarray, ache: np.ndarray, kappa: np.ndarray):
        fog_img = self.fog.apply(sigma, ache)
        glow_img = self.glow.apply(sigma, ache)
        bolt_img = self.lightning.apply(kappa)
        thunder_img = self.thunder.apply(kappa)
        wall_img = self.wall.apply(ache)

        frame = np.clip(
            fog_img.astype(np.uint16)
            + glow_img.astype(np.uint16)
            + bolt_img.astype(np.uint16)
            + thunder_img.astype(np.uint16)
            + wall_img.astype(np.uint16),
            0,
            255,
        ).astype(np.uint8)

        frame = self.motion.apply(frame)
        return frame
