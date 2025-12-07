from universe.physics.physics_world import PhysicsWorld
from universe.systems.base_system import System


class PhysicsSystemV3(System):
    """
    Bridges ECS world entities to the PhysicsWorld integrator.
    """

    def __init__(self, name: str = "physics_v3", order: int = 4, phase: str = "physics"):
        super().__init__(name=name, order=order, phase=phase)
        self.world = PhysicsWorld()

    def register(self, entity) -> None:
        self.world.add_entity(entity)

    def update(self, world, dt: float):
        # Ensure all entities with rigid bodies are known
        for ent in world.all_entities():
            self.world.add_entity(ent)
        self.world.step(dt)
