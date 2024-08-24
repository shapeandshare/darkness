from ..contracts.dtos.tiles.address import Address
from ..contracts.types.dao_document import DaoDocumentType


def address_type(address: Address) -> DaoDocumentType:
    if address.entity_id is not None:
        return DaoDocumentType.ENTITY
    elif address.tile_id is not None:
        return DaoDocumentType.TILE
    elif address.chunk_id is not None:
        return DaoDocumentType.CHUNK
    elif address.world_id is not None:
        return DaoDocumentType.WORLD

    raise Exception("Unknown address type")


def get_document_id_from_address(address: Address, doc_type: DaoDocumentType | None = None) -> str:
    if doc_type is None:
        doc_type = address_type(address)

    if doc_type == DaoDocumentType.ENTITY:
        return address.entity_id
    elif doc_type == DaoDocumentType.TILE:
        return address.tile_id
    elif doc_type == DaoDocumentType.CHUNK:
        return address.chunk_id
    elif doc_type == DaoDocumentType.WORLD:
        return address.world_id
    raise Exception("Unknown address type")
