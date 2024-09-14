from .tile import TileRequest


class TileGetRequest(TileRequest):

    # Used by command sdk
    full: bool | None = None
