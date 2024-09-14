from .chunk import ChunkRequest


class ChunkPatchRequest(ChunkRequest):
    partial: dict
