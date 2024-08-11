from ..types.tile import TileType
from .tiles.abtract import AbstractTile
from .tiles.tile import Tile


class Island(AbstractTile[str, Tile]):
    dimensions: tuple[int, int] | None = None
    biome: TileType | None = None
