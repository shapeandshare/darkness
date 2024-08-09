from pydantic import BaseModel

from .....dtos.world import World
from .....dtos.world_lite import WorldLite


class WorldGetResponse(BaseModel):
    world: World | WorldLite
