from universe.components.position import Position
from universe.render.camera import Camera
from universe.systems.base_system import System


class CameraSystem(System):
    """
    Camera that follows a target entity with smooth motion.
    """

    def __init__(self, universe, name: str = "camera", order: int = 150, phase: str = "logic"):
        super().__init__(name=name, order=order, phase=phase)
        self.universe = universe
        self.camera = Camera()
        self.target = None

    def follow(self, entity):
        self.target = entity

    def update(self, world, dt: float):
        if not self.target:
            return
        pos = self.target.get_component(Position)
        if not pos:
            return
        cx = pos.x - self.camera.width / 2
        cy = pos.y - self.camera.height / 2
        self.camera.move_towards(cx, cy)
