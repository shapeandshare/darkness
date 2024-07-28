from pydantic import BaseModel

from src.darkness.contracts.types.tile import TileType


class IslandCreateResponse(BaseModel):
    id: str
