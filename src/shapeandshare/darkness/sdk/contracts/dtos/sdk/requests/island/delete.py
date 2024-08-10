from pydantic import BaseModel


class IslandDeleteRequest(BaseModel):
    world_id: str
    island_id: str
