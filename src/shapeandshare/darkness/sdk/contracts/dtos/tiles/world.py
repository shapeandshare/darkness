from ...types.tile import TileType
from .abtract import AbstractTile
from .island import Island


class World(AbstractTile[str, Island]):
    """Basic World"""

    tile_type: TileType = TileType.WORLD
