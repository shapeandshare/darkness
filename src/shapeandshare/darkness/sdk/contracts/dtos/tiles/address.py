from pydantic import BaseModel


class Address(BaseModel):
    world_id: str | None = None
    chunk_id: str | None = None
    tile_id: str | None = None
    entity_id: str | None = None
