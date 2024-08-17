from pydantic import BaseModel

from ....tiles.world import World


class WorldGetResponse(BaseModel):
    world: World
