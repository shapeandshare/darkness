from pydantic import BaseModel


class Coordinate(BaseModel):
    # 2D
    x: int
    y: int
