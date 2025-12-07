from universe.world_v1.biome_map import BiomeMap
from universe.world_v1.climate import Climate
from universe.world_v1.daynight import DayNightCycle
from universe.world_v1.resource_spawner import ResourceSpawner
from universe.world_v1.season import SeasonCycle
from universe.world_v1.weather import Weather


class WorldSimV1:
    """
    High-level orchestrator for climate, seasons, weather, day/night, and resources.
    """

    def __init__(self, width: int = 200, height: int = 200):
        self.climate = Climate(width, height)
        self.seasons = SeasonCycle()
        self.biomes = BiomeMap()
        self.weather = Weather(width, height)
        self.daynight = DayNightCycle()
        self.spawner = ResourceSpawner()

    def step(self):
        season_shift = self.seasons.step()
        self.climate.update(season_shift)
        self.weather.update()
        light = self.daynight.step()

        return {
            "temperature": self.climate.temperature,
            "humidity": self.climate.humidity,
            "storms": self.weather.storms,
            "blooms": self.weather.coherence_blooms,
            "light": light,
        }
