from typing import TypeVar

from pydantic import BaseModel

from ...types.connection import TileConnectionType
from ...types.tile import TileType

KT = TypeVar("KT")
VT = TypeVar("VT")


class AbstractTile[KT, VT](BaseModel):
    id: str
    name: str | None = None
    rbac: dict = {}
    tile_type: TileType = TileType.UNKNOWN
    next: dict[TileConnectionType, str] = {}  # str=id
    contents: dict[KT, VT] = {}
    ids: set[KT] = set()
