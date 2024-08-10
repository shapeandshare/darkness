from pydantic import BaseModel


class WorldDeleteRequest(BaseModel):
    id: str
