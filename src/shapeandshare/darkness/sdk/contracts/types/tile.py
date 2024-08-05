from enum import Enum


class TileType(str, Enum):
    UNKNOWN = "unknown"

    OCEAN = "ocean"
    WATER = "water"

    SHORE = "shore"
    DIRT = "dirt"
    ROCK = "rock"
    GRASS = "grass"
    FOREST = "forest"
