from pydantic import BaseModel

from ..locations.island import Island


class IslandGetResponse(BaseModel):
    island: Island
