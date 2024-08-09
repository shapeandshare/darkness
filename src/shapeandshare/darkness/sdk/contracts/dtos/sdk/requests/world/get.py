from pydantic import BaseModel


class WorldGetRequest(BaseModel):
    id: str | None
