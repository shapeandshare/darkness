from ...types.tile import TileType
from .abtract import AbstractTile
from .chunk import Chunk


class World(AbstractTile[str, Chunk]):
    """Basic World"""

    tile_type: TileType = TileType.WORLD
