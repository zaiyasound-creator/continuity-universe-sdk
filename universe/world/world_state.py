from copy import deepcopy
from typing import Dict, Iterable, List, Optional

from universe.entities.entity import Entity


class WorldState:
    """
    Stores entities/components and time. Provides snapshot/restore for reversible stepping.
    """

    def __init__(self):
        self.time: float = 0.0
        self.entities: Dict[int, Entity] = {}
        self._next_entity_id: int = 1

    def advance_time(self, dt: float) -> None:
        self.time += dt

    def create_entity(self) -> Entity:
        eid = self._next_entity_id
        self._next_entity_id += 1
        entity = Entity(eid=eid)
        self.entities[eid] = entity
        return entity

    def remove_entity(self, entity_id: int) -> None:
        self.entities.pop(entity_id, None)

    def get_entity(self, entity_id: int) -> Optional[Entity]:
        return self.entities.get(entity_id)

    def all_entities(self) -> Iterable[Entity]:
        return self.entities.values()

    def snapshot(self):
        return {
            "time": self.time,
            "next_entity_id": self._next_entity_id,
            "entities": {eid: deepcopy(entity) for eid, entity in self.entities.items()},
        }

    def restore(self, snapshot):
        self.time = snapshot["time"]
        self._next_entity_id = snapshot["next_entity_id"]
        # Entities were deep-copied, so we can assign directly
        self.entities = snapshot["entities"]
