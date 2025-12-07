class BiomeMap:
    """
    Classifies world cells into biomes based on temperature and humidity.
    """

    def compute_biome(self, temp: float, humidity: float) -> str:
        if temp < 5:
            return "tundra"
        if temp < 15:
            return "forest" if humidity > 0.5 else "steppe"
        if temp < 28:
            return "grassland"
        if humidity < 0.3:
            return "desert"
        return "rainforest"
