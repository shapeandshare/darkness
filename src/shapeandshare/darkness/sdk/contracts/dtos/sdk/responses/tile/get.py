from pydantic import BaseModel

from ....tiles.tile import Tile


class TileGetResponse(BaseModel):
    tile: Tile
