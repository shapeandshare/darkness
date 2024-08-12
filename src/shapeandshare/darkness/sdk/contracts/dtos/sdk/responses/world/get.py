from pydantic import BaseModel

from ....tiles.world import World
from ....tiles.world_full import WorldFull


class WorldGetResponse(BaseModel):
    world: WorldFull | World
