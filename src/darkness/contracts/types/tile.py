from enum import Enum


class TileType(str, Enum):
    unknown = "unknown"

    water = "water"
    shore = "shore"
    dirt = "dirt"
    grass = "grass"
