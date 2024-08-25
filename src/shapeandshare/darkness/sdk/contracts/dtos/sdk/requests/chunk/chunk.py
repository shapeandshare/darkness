from pydantic import BaseModel


class ChunkRequest(BaseModel):
    world_id: str
    chunk_id: str
