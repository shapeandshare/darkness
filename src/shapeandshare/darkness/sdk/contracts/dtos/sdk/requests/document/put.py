from typing import TypeVar

from pydantic import BaseModel

from ....tiles.address import Address
from ...wrapped_data import WrappedData

T = TypeVar("T")


class DocumentPutRequest[T](BaseModel):
    address: Address
    wrapped_document: WrappedData[T]
