from universe.components.base_component import Component


class PatternComponent(Component):
    """Attach a pattern evaluator to an entity."""

    def __init__(self, pattern):
        self.pattern = pattern
