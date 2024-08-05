from pydantic import BaseModel

from ..dtos.entity import Entity
from ..types.connection import TileConnectionType
from ..types.tile import TileType


class Tile(BaseModel):
    id: str
    tile_type: TileType
    rbac: dict = {}
    next: dict[TileConnectionType, str] = {}  # str=id
    contains: dict[str, Entity] = {}  # str=id
