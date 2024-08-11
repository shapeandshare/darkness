from pydantic import BaseModel

from .....dtos.world import World
from .....dtos.world_full import WorldFull


class WorldGetResponse(BaseModel):
    world: WorldFull | World
