from .....types.chunk_quantum import ChunkQuantumType
from .chunk import ChunkRequest


class ChunkQuantumRequest(ChunkRequest):
    world_id: str | None = None
    chunk_id: str | None = None
    scope: ChunkQuantumType
