import logging
import os
import shutil
import uuid
from pathlib import Path

from ...sdk.contracts.dtos.entities.entity import Entity
from ...sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ...sdk.contracts.errors.server.dao.conflict import DaoConflictError
from ...sdk.contracts.errors.server.dao.doesnotexist import DaoDoesNotExistError
from ...sdk.contracts.errors.server.dao.inconsistency import DaoInconsistencyError
from .abstract import AbstractDao

logger = logging.getLogger()


class EntityDao(AbstractDao[Entity]):
    async def post(self, tokens: dict, document: Entity) -> WrappedData[Entity]:
        logger.debug("[EntityDAO] posting entity data to storage")
        tokens["entity_id"] = document.id
        entity_metadata_path: Path = self._document_path(tokens=tokens)
        if entity_metadata_path.exists():
            raise DaoConflictError("entity metadata already exists")
        if not entity_metadata_path.parents[2].exists():
            raise DaoDoesNotExistError("entity container (tile) does not exist")
        if not entity_metadata_path.parent.exists():
            logger.debug("[EntityDAO] entity metadata folder creating ..")
            entity_metadata_path.parent.mkdir(parents=True, exist_ok=True)
        nonce: str = str(uuid.uuid4())
        wrapped_data: WrappedData[Entity] = WrappedData[Entity](data=document, nonce=nonce)
        wrapped_data_raw: str = wrapped_data.model_dump_json(exclude_none=True)
        with open(file=entity_metadata_path, mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)
            os.fsync(file)

            # now validate we stored
        stored_entity: WrappedData[Entity] = await self.get(tokens=tokens)
        stored_entity.data = Entity.model_validate(stored_entity.data)
        if stored_entity.nonce != nonce:
            msg: str = f"storage inconsistency detected while storing entity {document.id} - nonce mismatch!"
            raise DaoInconsistencyError(msg)
        return stored_entity

    async def put(self, tokens: dict, wrapped_document: WrappedData[Entity]) -> WrappedData[Entity]:
        logger.debug("[EntityDAO] putting entity data to storage")
        tokens["tile_id"] = wrapped_document.data.id
        entity_metadata_path: Path = self._document_path(tokens=tokens)
        if not entity_metadata_path.parents[2].exists():
            raise DaoDoesNotExistError("entity container (tile) does not exist")
        if not entity_metadata_path.parent.exists():
            logger.debug("[EntityDAO] entity metadata folder creating ..")
            entity_metadata_path.parent.mkdir(parents=True, exist_ok=True)

        # see if we have a pre-existing nonce to verify against
        try:
            previous_state: WrappedData[Entity] = await self.get(tokens=tokens)
            previous_state.data = Entity.model_validate(previous_state.data)
            if previous_state.nonce != wrapped_document.nonce:
                msg: str = f"storage inconsistency detected while putting entity {wrapped_document.data.id} - nonce mismatch!"
                raise DaoInconsistencyError(msg)
        except DaoDoesNotExistError:
            # then no nonce to verify against.
            pass

        # if we made it this far we are safe to update

        nonce: str = str(uuid.uuid4())
        wrapped_data: WrappedData[Entity] = WrappedData[Entity](data=wrapped_document.data, nonce=nonce)
        wrapped_data_raw: str = wrapped_data.model_dump_json(exclude_none=True)
        with open(file=entity_metadata_path, mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)
            os.fsync(file)

        # now validate we stored
        stored_entity: WrappedData[Entity] = await self.get(tokens=tokens)
        stored_entity.data = Entity.model_validate(stored_entity.data)
        if stored_entity.nonce != nonce:
            msg: str = f"storage inconsistency detected while verifying put entity {wrapped_data.data.id} - nonce mismatch!"
            raise DaoInconsistencyError(msg)
        return stored_entity

    async def patch(self, tokens: dict, document: dict) -> WrappedData[Entity]:
        logger.debug("[EntityDAO] patching entity data to storage")
        if "id" in document:
            tokens["entity_id"] = document["id"]

        entity_metadata_path: Path = self._document_path(tokens=tokens)
        if not entity_metadata_path.parents[2].exists():
            raise DaoDoesNotExistError("entity container (tile) does not exist")
        if not entity_metadata_path.parent.exists():
            logger.debug("[EntityDAO] entity metadata folder creating ..")
            entity_metadata_path.parent.mkdir(parents=True, exist_ok=True)

        previous_state: WrappedData[Entity] = await self.get(tokens=tokens)
        previous_state.data = Entity.model_validate(previous_state.data)

        # if we made it this far we are safe to update

        # merge
        nonce: str = str(uuid.uuid4())
        previous_state_dict = previous_state.data.model_dump()
        new_state = EntityDao.recursive_dict_merge(previous_state_dict, document)
        wrapped_data: WrappedData[Entity] = WrappedData[Entity](data=new_state, nonce=nonce)

        # serialize to storage
        wrapped_data_raw: str = wrapped_data.model_dump_json(exclude_none=True)
        with open(file=entity_metadata_path, mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)
            os.fsync(file)

        # now validate we stored
        stored_entity: WrappedData[Entity] = await self.get(tokens=tokens)
        stored_entity.data = Entity.model_validate(stored_entity.data)
        if stored_entity.nonce != nonce:
            msg: str = f"storage inconsistency detected while verifying patched entity {wrapped_data.data.id} - nonce mismatch!"
            raise DaoInconsistencyError(msg)
        return stored_entity

    async def delete(self, tokens: dict) -> bool:
        logger.debug("[EntityDAO] deleting entity data from storage")
        entity_metadata_path: Path = self._document_path(tokens=tokens)
        if not entity_metadata_path.exists():
            raise DaoDoesNotExistError("entity metadata does not exist")
        # remove "entity_id"/ and lower
        shutil.rmtree(entity_metadata_path.parent)
        return True
