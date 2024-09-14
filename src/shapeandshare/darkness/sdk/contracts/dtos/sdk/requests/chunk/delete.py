from .chunk import ChunkRequest


class ChunkDeleteRequest(ChunkRequest):
    cascade: bool
    parent: bool
