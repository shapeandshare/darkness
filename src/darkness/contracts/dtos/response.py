from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Response(Generic[T], BaseModel):
    data: T
