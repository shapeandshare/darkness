from pydantic import BaseModel


class ChunkDeleteRequest(BaseModel):
    world_id: str
    chunk_id: str
