from pydantic import BaseModel


class IslandDeleteResponse(BaseModel):
    id: str
