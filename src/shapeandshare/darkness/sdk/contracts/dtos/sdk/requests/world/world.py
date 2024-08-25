from pydantic import BaseModel


class WorldRequest(BaseModel):
    id: str
