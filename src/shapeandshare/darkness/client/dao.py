import json

from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from ..sdk.common.utils import address_type, get_document_id_from_address
from ..sdk.contracts.dtos.entities.entity import Entity
from ..sdk.contracts.dtos.tiles.address import Address
from ..sdk.contracts.dtos.tiles.chunk import Chunk
from ..sdk.contracts.dtos.tiles.tile import Tile
from ..sdk.contracts.dtos.tiles.world import World
from ..sdk.contracts.types.dao_document import DaoDocumentType


def get_mongodb(hostname: str, port: int, database: str) -> Database:
    return MongoClient(hostname, port)[database]


class DaoClient(BaseModel):
    database: Database
    collections: dict[DaoDocumentType, Collection] = {}

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # our collections will match our document types
        for member in DaoDocumentType:
            # Create a collection for each document type
            self.collections[DaoDocumentType[member.name]] = self.database[member.value]

            # We add a single column index on the business logic layer `id` for our lookups:
            # db.<collection>.createIndex( { <field>: <sortOrder> } )
            self.collections[DaoDocumentType[member.name]].create_index({"id": 1})

    class Config:
        arbitrary_types_allowed = True

    # Single document delete
    async def delete(self, address: Address) -> DeleteResult:
        doc_type = address_type(address)
        document_id: str = get_document_id_from_address(address=address, doc_type=doc_type)
        return self.collections[doc_type].delete_one({"id": document_id})

    # single document get with typing!
    async def get(self, address: Address) -> World | Chunk | Tile | Entity:
        doc_type: DaoDocumentType = address_type(address=address)
        document_id: str = get_document_id_from_address(address=address, doc_type=doc_type)
        result: dict | None = self.collections[doc_type].find_one({"id": document_id})
        if result is None:
            raise Exception("no document found")
        if doc_type == DaoDocumentType.ENTITY:
            return Entity.model_validate(result)
        elif doc_type == DaoDocumentType.TILE:
            return Tile.model_validate(result)
        elif doc_type == DaoDocumentType.CHUNK:
            return Chunk.model_validate(result)
        elif doc_type == DaoDocumentType.WORLD:
            return World.model_validate(result)
        raise Exception("invalid document type")

    async def post(self, address: Address, document: World | Chunk | Tile | Entity) -> InsertOneResult:
        doc_type: DaoDocumentType = address_type(address=address)
        return self.collections[doc_type.value].insert_one(json.loads(document.model_dump_json()))

    async def patch(self, address: Address, document: dict) -> UpdateResult:
        # document CAN NOT CONTAIN set variables.  It MUST be serialized before this call, so help you
        doc_type: DaoDocumentType = address_type(address=address)
        document_id: str = get_document_id_from_address(address=address, doc_type=doc_type)
        return self.collections[doc_type.value].update_one(filter={"id": document_id}, update={"$set": document})
