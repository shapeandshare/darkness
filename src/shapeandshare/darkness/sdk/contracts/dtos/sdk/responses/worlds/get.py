from pydantic import BaseModel

from ....tiles.world import World


class WorldsGetResponse(BaseModel):
    worlds: list[World]
