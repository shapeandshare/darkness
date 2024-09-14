from .world import WorldRequest


class WorldDeleteRequest(WorldRequest):
    cascade: bool
