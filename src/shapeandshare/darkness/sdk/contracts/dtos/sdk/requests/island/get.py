from pydantic import BaseModel


class IslandGetRequest(BaseModel):
    world_id: str
    island_id: str

    # Used by command sdk
    full: bool | None = None
