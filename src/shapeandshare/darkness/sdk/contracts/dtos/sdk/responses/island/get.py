from pydantic import BaseModel

from ....tiles.island import Island

# from ....tiles.island_full import IslandFull


class IslandGetResponse(BaseModel):
    # island: IslandFull | Island
    island: Island
