class CollisionEvent:
    def __init__(self, entity_a, entity_b):
        self.a = entity_a
        self.b = entity_b


class TriggerEvent:
    def __init__(self, entity, trigger):
        self.entity = entity
        self.trigger = trigger
