from pydantic import BaseModel


class IslandGetRequest(BaseModel):
    world_id: str
    island_id: str
