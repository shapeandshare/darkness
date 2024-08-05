from pydantic import BaseModel

from ..types.tile import TileType
from .tile import Tile


class Island(BaseModel):
    id: str
    name: str
    rbac: dict = {}
    tiles: dict[str, Tile] = {}
    dimensions: tuple[int, int] | None = None
    biome: TileType | None = None
