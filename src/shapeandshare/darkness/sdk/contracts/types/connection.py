from enum import Enum
from typing import Self


class TileConnectionType(str, Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"

    # pylint: disable=no-else-return
    @classmethod
    def opposite(cls, of: Self) -> Self:
        if of == TileConnectionType.LEFT:
            return TileConnectionType.RIGHT
        elif of == TileConnectionType.RIGHT:
            return TileConnectionType.LEFT
        elif of == TileConnectionType.UP:
            return TileConnectionType.DOWN
        elif of == TileConnectionType.DOWN:
            return TileConnectionType.UP
        raise ValueError(f"Unknown tile connection type: {of}")
