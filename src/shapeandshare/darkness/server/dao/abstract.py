import logging
import os
import shutil
import uuid
from abc import abstractmethod
from enum import Enum
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel

from ...sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ...sdk.contracts.errors.server.dao.conflict import DaoConflictError
from ...sdk.contracts.errors.server.dao.doesnotexist import DaoDoesNotExistError
from ...sdk.contracts.errors.server.dao.inconsistency import DaoInconsistencyError

logger = logging.getLogger()

T = TypeVar("T")


class DocumentType(str, Enum):
    WORLD = "worlds"
    ISLAND = "islands"
    TILE = "tiles"
    ENTITY = "entities"


# class DocumentPath(BaseModel):
# tables = ["worlds", "islands", "tiles", "entities"]


class AbstractDao[T](BaseModel):
    storage_base_path: Path

    @staticmethod
    def recursive_dict_merge(dict1: dict, dict2: dict) -> dict:
        for key, value in dict2.items():
            if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
                # Recursively merge nested dictionaries
                dict1[key] = AbstractDao.recursive_dict_merge(dict1[key], value)
            else:
                # Merge non-dictionary values
                dict1[key] = value
        return dict1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage_base_path.mkdir(parents=True, exist_ok=True)

    def _document_path(self, tokens: dict) -> Path:
        path: Path = self.storage_base_path
        if "world_id" in tokens:
            path = path / "worlds" / tokens["world_id"]

        if "island_id" in tokens:
            path = path / "islands" / tokens["island_id"]

        if "tile_id" in tokens:
            path = path / "tiles" / tokens["tile_id"]

        if "entity_id" in tokens:
            path = path / "entities" / tokens["entity_id"]

        return path / "metadata.json"

    async def get(self, tokens: dict) -> WrappedData[T]:
        logger.debug("[AbstractDao] getting document metadata from storage")
        document_metadata_path: Path = self._document_path(tokens=tokens)
        if not document_metadata_path.exists():
            raise DaoDoesNotExistError("document metadata does not exist")
        with open(file=document_metadata_path, mode="r", encoding="utf-8") as file:
            os.fsync(file)
            json_data: str = file.read()
        return WrappedData[T].model_validate_json(json_data)

    @abstractmethod
    async def post(self, tokens: dict, document: T) -> WrappedData[T]:
        """ """

    async def post_partial(self, tokens: dict, document: T, exclude: dict | None = None) -> WrappedData[T]:
        entity_metadata_path: Path = self._document_path(tokens=tokens)
        if entity_metadata_path.exists():
            raise DaoConflictError("document metadata already exists")
        if not entity_metadata_path.parents[2].exists():
            raise DaoDoesNotExistError("document container does not exist")
        if not entity_metadata_path.parent.exists():
            logger.debug("[AbstractDao] document metadata folder creating ..")
            entity_metadata_path.parent.mkdir(parents=True, exist_ok=True)

        nonce: str = str(uuid.uuid4())
        wrapped_data: WrappedData[T] = WrappedData[T](data=document, nonce=nonce)
        dump_params: dict = {"exclude_none": True}
        if exclude is not None:
            dump_params["exclude"] = exclude
        wrapped_data_raw: str = wrapped_data.model_dump_json(**dump_params)
        with open(file=entity_metadata_path, mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)
            os.fsync(file)

        # now validate we stored
        stored_entity: WrappedData[T] = await self.get(tokens=tokens)
        if stored_entity.nonce != nonce:
            msg: str = f"storage inconsistency detected while storing document {document.id} - nonce mismatch!"
            raise DaoInconsistencyError(msg)
        return stored_entity

    @abstractmethod
    async def put(self, tokens: dict, wrapped_document: WrappedData[T]) -> WrappedData[T]:
        """ """

    async def put_partial(self, tokens: dict, wrapped_document: WrappedData[T], exclude: dict | None = None) -> WrappedData[T]:
        document_metadata_path: Path = self._document_path(tokens=tokens)
        if not document_metadata_path.parents[2].exists():
            raise DaoDoesNotExistError("document container does not exist")
        if not document_metadata_path.parent.exists():
            logger.debug("[AbstractDAO] document metadata folder creating ..")
            document_metadata_path.parent.mkdir(parents=True, exist_ok=True)

        # see if we have a pre-existing nonce to verify against
        try:
            previous_state: WrappedData[T] = await self.get(tokens=tokens)
            if previous_state.nonce != wrapped_document.nonce:
                msg: str = f"storage inconsistency detected while putting document {wrapped_document.data.id} - nonce mismatch!"
                raise DaoInconsistencyError(msg)
        except DaoDoesNotExistError:
            # then no nonce to verify against.
            pass

        # if we made it this far we are safe to update

        nonce: str = str(uuid.uuid4())
        wrapped_data: WrappedData[T] = WrappedData[T](data=wrapped_document.data, nonce=nonce)
        dump_params: dict = {"exclude_none": True}
        if exclude is not None:
            dump_params["exclude"] = exclude
        wrapped_data_raw: str = wrapped_data.model_dump_json(**dump_params)
        with open(file=document_metadata_path, mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)
            os.fsync(file)

        # now validate we stored
        stored_entity: WrappedData[T] = await self.get(tokens=tokens)
        if stored_entity.nonce != nonce:
            msg: str = f"storage inconsistency detected while verifying put entity {wrapped_data.data.id} - nonce mismatch!"
            raise DaoInconsistencyError(msg)
        return stored_entity

    @abstractmethod
    async def patch(self, tokens: dict, document: dict) -> WrappedData[T]:
        """ """

    async def patch_partial(self, tokens: dict, document: dict, exclude: dict | None = None) -> WrappedData[T]:
        logger.debug("[AbstractDAO] patching document data in storage")
        document_metadata_path: Path = self._document_path(tokens=tokens)
        if not document_metadata_path.parents[2].exists():
            raise DaoDoesNotExistError("document container does not exist")
        if not document_metadata_path.parent.exists():
            logger.debug("[WorldDAO] document metadata folder creating ..")
            document_metadata_path.parent.mkdir(parents=True, exist_ok=True)

        previous_state: WrappedData[T] = await self.get(tokens=tokens)

        # if we made it this far we are safe to update

        # merge
        nonce: str = str(uuid.uuid4())
        previous_state_dict = previous_state.data
        new_state = AbstractDao.recursive_dict_merge(previous_state_dict, document)
        wrapped_data: WrappedData[T] = WrappedData[T](data=new_state, nonce=nonce)

        # serialize to storage
        dump_params: dict = {"exclude_none": True}
        if exclude is not None:
            dump_params["exclude"] = exclude
        wrapped_data_raw: str = wrapped_data.model_dump_json(**dump_params)
        with open(file=document_metadata_path, mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)
            os.fsync(file)

        # now validate we stored
        stored_entity: WrappedData[T] = await self.get(tokens=tokens)
        if stored_entity.nonce != nonce:
            msg: str = f"storage inconsistency detected while verifying patched document {wrapped_data.data.id} - nonce mismatch!"
            raise DaoInconsistencyError(msg)
        return stored_entity

    async def delete(self, tokens: dict) -> bool:
        logger.debug("[AbstractDAO] deleting document data from storage")
        document_metadata_path: Path = self._document_path(tokens=tokens)
        if not document_metadata_path.exists():
            raise DaoDoesNotExistError("document metadata does not exist")
        shutil.rmtree(document_metadata_path.parent)
        return True
