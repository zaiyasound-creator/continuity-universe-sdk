from universe.components.ai_state import AIState
from universe.systems.base_system import System


class AIStateSystem(System):
    """
    Simple finite state machine progression.
    """

    def __init__(self, name: str = "ai_state", order: int = 30, phase: str = "logic"):
        super().__init__(name=name, order=order, phase=phase)

    def update(self, world, dt: float):
        for entity in world.all_entities():
            state = entity.get_component(AIState)
            if not state:
                continue
            state.timer += dt
            if state.state == "idle" and state.timer > 2.0:
                state.state = "wandering"
                state.timer = 0.0
            elif state.state == "wandering" and state.timer > 3.0:
                state.state = "idle"
                state.timer = 0.0
