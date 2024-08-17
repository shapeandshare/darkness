from enum import Enum


class TileType(str, Enum):
    WORLD = "world"
    CHUNK = "chunk"

    UNKNOWN = "unknown"

    OCEAN = "ocean"
    WATER = "water"

    SHORE = "shore"
    DIRT = "dirt"
    ROCK = "rock"
    GRASS = "grass"
    FOREST = "forest"
