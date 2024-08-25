from .chunk import ChunkRequest


class ChunkGetRequest(ChunkRequest):

    # Used by command sdk
    full: bool | None = None
