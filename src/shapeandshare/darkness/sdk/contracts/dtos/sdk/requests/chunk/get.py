from pydantic import BaseModel


class ChunkGetRequest(BaseModel):
    world_id: str
    chunk_id: str

    # Used by command sdk
    full: bool | None = None
