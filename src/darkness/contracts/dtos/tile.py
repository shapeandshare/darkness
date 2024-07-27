from pydantic import BaseModel

from ..types.connection import TileConnectionType
from ..types.tile import TileType


class Tile(BaseModel):
    id: str
    tileType: TileType
    rbac: dict = {}
    next: dict[TileConnectionType, str] = {} # str=id
    # subtype: ClassVar[str]
    # subtype: any | None = None


