from pydantic import BaseModel


class IslandGetRequest(BaseModel):
    id: str
