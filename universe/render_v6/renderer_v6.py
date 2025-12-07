import numpy as np

from universe.render.composite_cpu import CompositeCPU
from universe.render.heatmap_cpu import HeatmapCPU
from universe.render_v6.agent_glow import AgentGlow
from universe.render_v6.bloom_shader import AetherBloom
from universe.render_v6.curvature_halo import CurvatureHalo
from universe.render_v6.flow_distortion import FlowDistortion
from universe.render_v6.temporal_accumulator import TemporalAccumulator


class RendererV6:
    """
    Cinematic renderer combining heatmaps, halos, distortion, bloom, and trails.
    """

    def __init__(self, width: int, height: int):
        self.surface = np.zeros((height, width, 3), np.uint8)

        self.temporal = TemporalAccumulator(width, height)
        self.bloom = AetherBloom()
        self.halo = CurvatureHalo()
        self.distort = FlowDistortion()
        self.agentglow = AgentGlow()
        self.composite = CompositeCPU()
        self.heatmap = HeatmapCPU()

    def render(self, sigma, kappa, ache, phi_x, phi_y, agents):
        # σ base heatmap
        base = self.heatmap.render(sigma)

        # curvature halo
        halo_map = self.halo.apply(kappa)
        halo_img = np.stack([halo_map] * 3, axis=-1)

        out = self.composite.composite(base, halo_img)

        # distortion by flow
        out = self.distort.apply(out, phi_x, phi_y)

        # bloom
        out = self.bloom.apply(out)

        # agent glow
        out = self.agentglow.apply(out, agents)

        # temporal trails
        out = self.temporal.accumulate(out)

        self.surface = out
        return out

    def get_frame(self):
        return self.surface
