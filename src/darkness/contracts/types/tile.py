from enum import Enum


class TileType(str, Enum):
    UNKNOWN = "unknown"

    WATER = "water"
    SHORE = "shore"
    DIRT = "dirt"
    GRASS = "grass"
