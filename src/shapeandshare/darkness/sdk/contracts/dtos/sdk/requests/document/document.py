from pydantic import BaseModel

from ....tiles.address import Address


class DocumentRequest(BaseModel):
    address: Address
    full: bool = False
