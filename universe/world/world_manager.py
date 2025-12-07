from typing import Dict

from universe.world.world_state import WorldState


class WorldManager:
    """
    Registry for multiple worlds/universes.
    """

    def __init__(self):
        self._worlds: Dict[str, WorldState] = {}
        self._active: str = "default"
        self._worlds[self._active] = WorldState()

    def create_world(self, name: str) -> WorldState:
        world = WorldState()
        self._worlds[name] = world
        self._active = name
        return world

    def get_world(self, name: str) -> WorldState:
        return self._worlds[name]

    def active_world(self) -> WorldState:
        return self._worlds[self._active]

    def set_active(self, name: str) -> WorldState:
        if name not in self._worlds:
            raise KeyError(f"World '{name}' not found")
        self._active = name
        return self._worlds[name]

    def snapshot(self):
        return {name: world.snapshot() for name, world in self._worlds.items()}

    def restore(self, snapshot):
        self._worlds = {}
        for name, world_state in snapshot.items():
            world = WorldState()
            world.restore(world_state)
            self._worlds[name] = world
        # Reset active to first key
        if snapshot:
            self._active = next(iter(snapshot.keys()))
