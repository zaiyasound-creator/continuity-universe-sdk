from universe.components.base_component import Component


class Mass(Component):
    """Mass scalar for physics computations."""

    def __init__(self, value: float = 1.0):
        self.value = value
