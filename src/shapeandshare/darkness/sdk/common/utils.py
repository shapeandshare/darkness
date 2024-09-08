import secrets

from ..contracts.dtos.tiles.address import Address
from ..contracts.errors.server.dao.unknown import DaoUnknownError
from ..contracts.types.dao_document import DaoDocumentType


def address_type(address: Address) -> DaoDocumentType:
    if address.entity_id is not None:
        return DaoDocumentType.ENTITY

    if address.tile_id is not None:
        return DaoDocumentType.TILE

    if address.chunk_id is not None:
        return DaoDocumentType.CHUNK

    if address.world_id is not None:
        return DaoDocumentType.WORLD

    raise DaoUnknownError("invalid document type")


def get_document_id_from_address(address: Address, doc_type: DaoDocumentType | None = None) -> str:
    if doc_type is None:
        doc_type = address_type(address)

    if doc_type == DaoDocumentType.ENTITY:
        return address.entity_id

    if doc_type == DaoDocumentType.TILE:
        return address.tile_id

    if doc_type == DaoDocumentType.CHUNK:
        return address.chunk_id

    if doc_type == DaoDocumentType.WORLD:
        return address.world_id

    raise DaoUnknownError("invalid document type")


def generate_random_float(min_val=0.0, max_val=1.0) -> float:
    # Generation of 16-bit random integer
    random_int: int = secrets.randbelow(2**16)
    random_float: float = min_val + ((max_val - min_val) * (random_int / (2**16)))
    return random_float
