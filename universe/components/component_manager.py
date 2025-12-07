from typing import Dict, Iterable, Optional, Type, TypeVar

from universe.components.base_component import Component
from universe.engine.event_bus import EventBus
from universe.entities.entity import Entity


C = TypeVar("C", bound=Component)


class ComponentManager:
    """
    Tracks components per entity and per type, and emits component change events.
    """

    def __init__(self, event_bus: Optional[EventBus] = None):
        self._by_entity: Dict[int, Dict[Type[Component], Component]] = {}
        self._by_type: Dict[Type[Component], Dict[int, Component]] = {}
        self.event_bus = event_bus

    def add(self, entity: Entity, component: C) -> C:
        eid = entity.id
        if eid is None:
            raise ValueError("Entity must have an id before adding components")

        self._by_entity.setdefault(eid, {})[type(component)] = component
        self._by_type.setdefault(type(component), {})[eid] = component

        entity.add_component(component)
        if self.event_bus:
            self.event_bus.publish("component_changed", {"entity_id": eid, "component": component})
        return component

    def remove(self, entity: Entity, component_type: Type[C]) -> None:
        eid = entity.id
        if eid is None:
            return
        self._by_entity.get(eid, {}).pop(component_type, None)
        self._by_type.get(component_type, {}).pop(eid, None)
        entity.remove_component(component_type)
        if self.event_bus:
            self.event_bus.publish("component_changed", {"entity_id": eid, "component": None})

    def get(self, entity: Entity, component_type: Type[C]) -> Optional[C]:
        eid = entity.id
        if eid is None:
            return None
        return self._by_entity.get(eid, {}).get(component_type)  # type: ignore[return-value]

    def all_for_entity(self, entity: Entity) -> Iterable[Component]:
        eid = entity.id
        if eid is None:
            return []
        return self._by_entity.get(eid, {}).values()

    def entities_with(self, component_type: Type[C]) -> Iterable[tuple[int, C]]:
        return list((eid, comp) for eid, comp in self._by_type.get(component_type, {}).items())

    def snapshot(self):
        # Components are stored by reference; assume Component.snapshot is lightweight.
        return {
            "by_entity": {
                eid: {ctype.__name__: comp.snapshot() for ctype, comp in comps.items()}
                for eid, comps in self._by_entity.items()
            }
        }

    def restore(self, snapshot) -> None:
        self._by_entity = {}
        self._by_type = {}
        # Note: without a registry of component classes, restore only rebuilds per-entity dict shape.
        for eid_str, comp_map in snapshot.get("by_entity", {}).items():
            eid = int(eid_str)
            self._by_entity[eid] = {}
            for _name, _state in comp_map.items():
                # Placeholder: real restore would need component class lookup
                # Skipping actual rehydration to avoid guessing types.
                pass
