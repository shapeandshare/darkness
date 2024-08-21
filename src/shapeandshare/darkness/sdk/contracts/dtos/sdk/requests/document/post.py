from typing import TypeVar

from pydantic import BaseModel

from ....tiles.address import Address

T = TypeVar("T")


class DocumentPostRequest[T](BaseModel):
    address: Address
    document: T
