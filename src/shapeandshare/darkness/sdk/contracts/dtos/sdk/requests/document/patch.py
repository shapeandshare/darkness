from pydantic import BaseModel

from ....tiles.address import Address


class DocumentPatchRequest(BaseModel):
    address: Address
    document: dict
