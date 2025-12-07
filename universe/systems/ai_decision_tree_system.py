from universe.components.ai_decision_tree import DecisionNode
from universe.systems.base_system import System


class AIDecisionTreeSystem(System):
    """
    Evaluates decision nodes and advances to returned branch.
    """

    def __init__(self, name: str = "ai_decision_tree", order: int = 25, phase: str = "logic"):
        super().__init__(name=name, order=order, phase=phase)

    def update(self, world, dt: float):
        for entity in world.all_entities():
            node = entity.get_component(DecisionNode)
            if not node:
                continue
            next_node = node.evaluate(entity, world)
            if next_node:
                entity.add_component(next_node)
