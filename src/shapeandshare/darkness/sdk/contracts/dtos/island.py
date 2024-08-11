# from pydantic import BaseModel

from .tiles.abtract import AbstractTile
from .tiles.tile import Tile
from ..types.tile import TileType


# class Island(BaseModel):
#     id: str
#     name: str
#     rbac: dict = {}
#     ids: set[str] = set()
#     dimensions: tuple[int, int] | None = None
#     biome: TileType | None = None

class Island(AbstractTile[str, Tile]):
    # id: str
    # name: str
    # rbac: dict = {}
    # ids: set[str] = set()
    dimensions: tuple[int, int] | None = None
    biome: TileType | None = None
