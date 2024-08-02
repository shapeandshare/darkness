from pydantic import BaseModel

from ...types.tile import TileType


class IslandDeleteRequest(BaseModel):
    id: str
