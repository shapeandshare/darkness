from pydantic import BaseModel


class TileRequest(BaseModel):
    world_id: str
    chunk_id: str
    tile_id: str
