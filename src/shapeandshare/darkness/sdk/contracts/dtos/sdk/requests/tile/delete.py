from .tile import TileRequest


class TileDeleteRequest(TileRequest):
    cascade: bool
    parent: bool
