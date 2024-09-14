from pydantic import BaseModel


class EntityRequest(BaseModel):
    world_id: str
    chunk_id: str
    tile_id: str
    entity_id: str
