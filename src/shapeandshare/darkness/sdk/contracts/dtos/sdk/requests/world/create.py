from pydantic import BaseModel


class WorldCreateRequest(BaseModel):
    name: str | None
