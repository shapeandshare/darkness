from pydantic import BaseModel


class IslandsGetResponse(BaseModel):
    ids: list[str]
