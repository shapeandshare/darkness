from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class WrappedData(BaseModel, Generic[T]):
    data: T
    nonce: str
