from enum import Enum


class TileConnectionType(str, Enum):
    left = "left"
    right = "right"
    up = "up"
    down = "down"
