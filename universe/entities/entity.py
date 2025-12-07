class Entity:
    def __init__(self, eid: int):
        self.id = eid
        self.components = {}

    def add(self, component):
        self.components[type(component)] = component

    def get(self, comp_type):
        return self.components.get(comp_type)

    def remove(self, comp_type):
        self.components.pop(comp_type, None)
