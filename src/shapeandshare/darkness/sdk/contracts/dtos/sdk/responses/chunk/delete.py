from pydantic import BaseModel


class ChunkDeleteResponse(BaseModel):
    id: str
