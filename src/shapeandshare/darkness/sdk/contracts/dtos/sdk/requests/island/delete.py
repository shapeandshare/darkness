from pydantic import BaseModel


class IslandDeleteRequest(BaseModel):
    id: str
