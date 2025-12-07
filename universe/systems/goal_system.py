from universe.components.goal_component import GoalComponent
from universe.systems.base_system import System


class GoalSystem(System):
    """
    Accumulates goal progress using a provided goal function.
    """

    def __init__(self, name: str = "goals", order: int = 40, phase: str = "logic"):
        super().__init__(name=name, order=order, phase=phase)

    def update(self, world, dt: float):
        for entity in world.all_entities():
            goal = entity.get_component(GoalComponent)
            if not goal:
                continue
            goal.progress += goal.goal_fn(entity, world) * dt
