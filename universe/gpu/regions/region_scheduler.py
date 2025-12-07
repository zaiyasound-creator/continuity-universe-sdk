try:
    from numba import cuda
except Exception:
    cuda = None


class RegionScheduler:
    """
    Multi-region orchestrator: steps all regions, handles migration.
    """

    def __init__(self, region_map, gpu_context):
        """
        region_map: dict[(ix, iy)] = RegionState
        """
        self.region_map = region_map
        self.gpu_context = gpu_context

        for region in region_map.values():
            gpu_context.assign_stream(region)

    def step(self, dt: float):
        # Launch all regions; if CUDA streams exist, use them, else serial
        if cuda is not None:
            # Use streams to overlap; region.step uses default stream so this is best-effort
            for region in self.region_map.values():
                stream = region.cuda_stream
                if stream is None:
                    region.step(dt)
                else:
                    stream.run(region.step, dt) if hasattr(stream, "run") else region.step(dt)
            self.gpu_context.wait_all()
        else:
            for region in self.region_map.values():
                region.step(dt)

        self._resolve_region_transfers()

    def _resolve_region_transfers(self):
        for key, region in self.region_map.items():
            x0, y0, x1, y1 = region.bounds
            width = x1 - x0
            height = y1 - y0
            move_list = []
            for eid, ent in region.entities.items():
                pos = ent.get("Position")
                if pos is None:
                    continue
                if pos.x < x0 or pos.x >= x1 or pos.y < y0 or pos.y >= y1:
                    move_list.append(eid)

            for eid in move_list:
                ent = region.entities.pop(eid)
                pos = ent.get("Position")
                tx = int(pos.x // width)
                ty = int(pos.y // height)
                target = self.region_map.get((tx, ty))
                if target:
                    target.entities[eid] = ent
