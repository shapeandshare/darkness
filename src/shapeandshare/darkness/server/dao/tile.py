import logging
import os
import shutil
import uuid
from copy import deepcopy
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel

from ...sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ...sdk.contracts.dtos.tiles.address import Address
from ...sdk.contracts.errors.server.dao.conflict import DaoConflictError
from ...sdk.contracts.errors.server.dao.doesnotexist import DaoDoesNotExistError
from ...sdk.contracts.errors.server.dao.inconsistency import DaoInconsistencyError

logger = logging.getLogger()

T = TypeVar("T")


class TileDao[T](BaseModel):
    storage_base_path: Path

    @staticmethod
    def recursive_dict_merge(dict1: dict, dict2: dict) -> dict:
        for key, value in dict2.items():
            if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
                # Recursively merge nested dictionaries
                dict1[key] = TileDao.recursive_dict_merge(dict1[key], value)
            else:
                # Merge non-dictionary values
                dict1[key] = value
        return dict1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage_base_path.mkdir(parents=True, exist_ok=True)

    def _document_path(self, address: Address) -> Path:
        return self.storage_base_path / address.resolve()

    def _assert_metadata_exists(self, address: Address) -> Path:
        document_metadata_path: Path = self._document_path(address=address)
        if not document_metadata_path.exists():
            raise DaoDoesNotExistError("document metadata does not exist")
        return document_metadata_path

    def _assert_metadata_does_not_exists(self, address: Address) -> Path:
        document_metadata_path: Path = self._document_path(address=address)
        if document_metadata_path.exists():
            raise DaoConflictError("document metadata already exists")
        return document_metadata_path

    def _assert_metadata_parent_exists(self, address: Address) -> Path:
        document_metadata_path: Path = self._document_path(address=address)
        if not document_metadata_path.parents[2].exists():
            raise DaoDoesNotExistError("document container does not exist")
        return document_metadata_path

    @staticmethod
    def _safe_create(document_metadata_path: Path):
        if not document_metadata_path.parent.exists():
            document_metadata_path.parent.mkdir(parents=True, exist_ok=True)

    async def get(self, address: Address) -> WrappedData[T]:
        address_copy = deepcopy(address)
        document_metadata_path: Path = self._assert_metadata_exists(address=address_copy)
        with open(file=document_metadata_path, mode="r", encoding="utf-8") as file:
            os.fsync(file)
            json_data: str = file.read()
        return WrappedData[T].model_validate_json(json_data)

    async def post(self, address: Address, document: T, exclude: dict | None = None) -> WrappedData[T]:
        address_copy = deepcopy(address)

        self._assert_metadata_does_not_exists(address=address_copy)
        document_metadata_path: Path = self._assert_metadata_parent_exists(address=address_copy)
        TileDao._safe_create(document_metadata_path=document_metadata_path)

        nonce: str = str(uuid.uuid4())
        wrapped_data: WrappedData[T] = WrappedData[T](data=document, nonce=nonce)
        dump_params: dict = {"exclude_none": True}  # exclude `None`
        dump_params["exclude"] = {"data": {"contents"}}  # default exclude contents
        if exclude is not None:
            dump_params["exclude"] = exclude
        wrapped_data_raw: str = wrapped_data.model_dump_json(**dump_params)
        with open(file=document_metadata_path, mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)
            os.fsync(file)

        # now validate we stored
        stored_entity: WrappedData[T] = await self.get(address=address_copy)
        if stored_entity.nonce != nonce:
            msg: str = f"storage inconsistency detected while storing document {document.id} - nonce mismatch!"
            raise DaoInconsistencyError(msg)
        return stored_entity

    async def put(
        self, address: Address, wrapped_document: WrappedData[T], exclude: dict | None = None
    ) -> WrappedData[T]:
        address_copy = deepcopy(address)

        document_metadata_path: Path = self._assert_metadata_exists(address=address_copy)

        # see if we have a pre-existing nonce to verify against
        try:
            previous_state: WrappedData[T] = await self.get(address=address_copy)
            if previous_state.nonce != wrapped_document.nonce:
                msg: str = (
                    f"storage inconsistency detected while putting document {wrapped_document.data.id} - nonce mismatch!"
                )
                raise DaoInconsistencyError(msg)
        except DaoDoesNotExistError:
            # then no nonce to verify against.
            pass

        # if we made it this far we are safe to update

        nonce: str = str(uuid.uuid4())
        wrapped_data: WrappedData[T] = WrappedData[T](data=wrapped_document.data, nonce=nonce)
        dump_params: dict = {"exclude_none": True}  # exclude `None`
        dump_params["exclude"] = {"data": {"contents"}}  # default exclude contents
        if exclude is not None:
            dump_params["exclude"] = exclude
        wrapped_data_raw: str = wrapped_data.model_dump_json(**dump_params)
        with open(file=document_metadata_path, mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)
            os.fsync(file)

        # now validate we stored
        stored_entity: WrappedData[T] = await self.get(address=address_copy)
        if stored_entity.nonce != nonce:
            msg: str = (
                f"storage inconsistency detected while verifying put entity {wrapped_data.data.id} - nonce mismatch!"
            )
            raise DaoInconsistencyError(msg)
        return stored_entity

    async def patch(self, address: Address, document: dict, exclude: dict | None = None) -> WrappedData[T]:
        address_copy = deepcopy(address)
        document_copy = deepcopy(document)
        if "id" in document_copy:
            del document_copy["id"]

        document_metadata_path: Path = self._assert_metadata_exists(address=address_copy)
        previous_state: WrappedData[T] = await self.get(address=address_copy)

        # if we made it this far we are safe to update

        # merge
        nonce: str = str(uuid.uuid4())
        previous_state_dict = previous_state.data
        new_state = TileDao.recursive_dict_merge(previous_state_dict, document_copy)
        wrapped_data: WrappedData[T] = WrappedData[T](data=new_state, nonce=nonce)

        # serialize to storage
        dump_params: dict = {"exclude_none": True}  # exclude `None`
        dump_params["exclude"] = {"data": {"contents"}}  # default exclude contents
        if exclude is not None:
            dump_params["exclude"] = exclude
        wrapped_data_raw: str = wrapped_data.model_dump_json(**dump_params)
        with open(file=document_metadata_path, mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)
            os.fsync(file)

        # now validate we stored
        stored_entity: WrappedData[T] = await self.get(address=address_copy)
        if stored_entity.nonce != nonce:
            msg: str = (
                f"storage inconsistency detected while verifying patched document {wrapped_data.data.id} - nonce mismatch!"
            )
            raise DaoInconsistencyError(msg)
        return stored_entity

    async def delete(self, address: Address) -> bool:
        document_metadata_path: Path = self._assert_metadata_exists(address=address)
        shutil.rmtree(document_metadata_path.parent)
        return True
