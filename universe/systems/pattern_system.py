from universe.components.pattern_component import PatternComponent
from universe.systems.base_system import System


class PatternSystem(System):
    """
    Evaluates pattern components after physics.
    """

    def __init__(self, name: str = "patterns", order: int = 50, phase: str = "patterns"):
        super().__init__(name=name, order=order, phase=phase)

    def update(self, world, dt: float):
        for entity in world.all_entities():
            pattern_comp = entity.get_component(PatternComponent)
            if pattern_comp:
                pattern = pattern_comp.pattern
                evaluator = getattr(pattern, "evaluate", None) or getattr(pattern, "step", None)
                if callable(evaluator):
                    evaluator(world, dt)
