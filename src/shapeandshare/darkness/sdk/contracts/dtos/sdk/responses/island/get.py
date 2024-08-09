from pydantic import BaseModel

from .....dtos.island import Island
from ....island_lite import IslandLite


class IslandGetResponse(BaseModel):
    island: Island | IslandLite
