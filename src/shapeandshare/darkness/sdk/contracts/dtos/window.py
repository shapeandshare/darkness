from pydantic import BaseModel

from .coordinate import Coordinate


class Window(BaseModel):
    # 2D window
    min: Coordinate
    max: Coordinate
