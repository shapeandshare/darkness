from pydantic import BaseModel


class ChunkCreateResponse(BaseModel):
    id: str
