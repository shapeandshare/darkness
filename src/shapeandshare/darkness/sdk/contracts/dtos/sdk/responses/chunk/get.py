from pydantic import BaseModel

from ....tiles.chunk import Chunk


class ChunkGetResponse(BaseModel):
    chunk: Chunk
