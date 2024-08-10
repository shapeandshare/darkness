from pydantic import BaseModel


class WorldCreateResponse(BaseModel):
    id: str
