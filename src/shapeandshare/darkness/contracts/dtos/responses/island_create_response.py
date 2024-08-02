from pydantic import BaseModel


class IslandCreateResponse(BaseModel):
    id: str
