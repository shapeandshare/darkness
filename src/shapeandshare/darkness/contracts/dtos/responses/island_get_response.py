from pydantic import BaseModel

from ..island import Island


class IslandGetResponse(BaseModel):
    island: Island
