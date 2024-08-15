import logging
import os
import uuid
from pathlib import Path

from pydantic import BaseModel

from ...sdk.contracts.dtos.entities.entity import Entity
from ...sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ...sdk.contracts.errors.server.dao.conflict import DaoConflictError
from ...sdk.contracts.errors.server.dao.doesnotexist import DaoDoesNotExistError
from ...sdk.contracts.errors.server.dao.inconsistency import DaoInconsistencyError

logger = logging.getLogger()


class EntityDao(BaseModel):
    # ["base"] / "worlds" / "wold_id" / "islands" / "island_id" / "tiles" / "tile_id" / "entities" / "entity_id" / "metadata.json"
    storage_base_path: Path

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage_base_path.mkdir(parents=True, exist_ok=True)

    ### Internal ##################################

    def _entity_path(self, world_id: str, island_id: str, tile_id: str, entity_id: str) -> Path:
        # ["base"] / "worlds" / "wold_id" / "islands" / "island_id" / "tiles" / "tile_id" / "entities" / "entity_id" / "{entity_id}.json"
        return self.storage_base_path / "worlds" / world_id / "islands" / island_id / "tiles" / tile_id / "entities" / entity_id / "metadata.json"

    async def get(self, world_id: str, island_id: str, tile_id: str, entity_id: str) -> WrappedData[Entity]:
        logger.debug("[EntityDAO] getting entity data from storage")
        entity_metadata_path: Path = self._entity_path(world_id=world_id, island_id=island_id, tile_id=tile_id, entity_id=entity_id)
        if not entity_metadata_path.exists():
            raise DaoDoesNotExistError("entity metadata does not exist")
        with open(file=entity_metadata_path, mode="r", encoding="utf-8") as file:
            os.fsync(file)
            json_data: str = file.read()
        return WrappedData[Entity].model_validate_json(json_data)

    async def post(self, world_id: str, island_id: str, tile_id: str, entity: Entity) -> None:
        logger.debug("[EntityDAO] posting entity data to storage")
        entity_metadata_path: Path = self._entity_path(world_id=world_id, island_id=island_id, tile_id=tile_id, entity_id=entity.id)
        if entity_metadata_path.exists():
            raise DaoConflictError("entity metadata already exists")
        if not entity_metadata_path.parents[2].exists():
            raise DaoDoesNotExistError("entity container (tile) does not exist")
        if not entity_metadata_path.parent.exists():
            logger.debug("[EntityDAO] entity metadata folder creating ..")
            entity_metadata_path.parent.mkdir(parents=True, exist_ok=True)
        nonce: str = str(uuid.uuid4())
        wrapped_data: WrappedData[Entity] = WrappedData[Entity](data=entity, nonce=nonce)
        wrapped_data_raw: str = wrapped_data.model_dump_json(exclude_none=True)
        with open(file=entity_metadata_path, mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)
            os.fsync(file)

            # now validate we stored
        stored_entity: WrappedData[Entity] = await self.get(world_id=world_id, island_id=island_id, tile_id=tile_id, entity_id=entity.id)
        if stored_entity.nonce != nonce:
            msg: str = f"storage inconsistency detected while storing entity {entity.id} - nonce mismatch!"
            raise DaoInconsistencyError(msg)

    async def put_safe(self, world_id: str, island_id: str, tile_id: str, wrapped_entity: WrappedData[Entity]) -> None:
        logger.debug("[EntityDAO] putting entity data to storage")
        entity_metadata_path: Path = self._entity_path(world_id=world_id, island_id=island_id, tile_id=tile_id, entity_id=wrapped_entity.data.id)
        if not entity_metadata_path.parents[2].exists():
            raise DaoDoesNotExistError("entity container (tile) does not exist")
        if not entity_metadata_path.parent.exists():
            logger.debug("[EntityDAO] entity metadata folder creating ..")
            entity_metadata_path.parent.mkdir(parents=True, exist_ok=True)

        # see if we have a pre-existing nonce to verify against
        try:
            previous_state: WrappedData[Entity] = await self.get(world_id=world_id, island_id=island_id, tile_id=tile_id, entity_id=wrapped_entity.data.id)
            if previous_state.nonce != wrapped_entity.nonce:
                msg: str = f"storage inconsistency detected while putting entity {wrapped_entity.data.id} - nonce mismatch!"
                raise DaoInconsistencyError(msg)
        except DaoDoesNotExistError:
            # then no nonce to verify against.
            pass

        # if we made it this far we are safe to update

        nonce: str = str(uuid.uuid4())
        wrapped_data: WrappedData[Entity] = WrappedData[Entity](data=wrapped_entity.data, nonce=nonce)
        wrapped_data_raw: str = wrapped_data.model_dump_json(exclude_none=True)
        with open(file=entity_metadata_path, mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)
            os.fsync(file)

        # now validate we stored
        stored_entity: WrappedData[Entity] = await self.get(world_id=world_id, island_id=island_id, tile_id=tile_id, entity_id=wrapped_data.data.id)
        if stored_entity.nonce != nonce:
            msg: str = f"storage inconsistency detected while verifying put entity {wrapped_data.data.id} - nonce mismatch!"
            raise DaoInconsistencyError(msg)

    async def delete(self, world_id: str, island_id: str, tile_id: str, entity_id: str) -> None:
        logger.debug("[EntityDAO] deleting entity data from storage")
        entity_metadata_path: Path = self._entity_path(world_id=world_id, island_id=island_id, tile_id=tile_id, entity_id=entity_id)
        if not entity_metadata_path.exists():
            raise DaoDoesNotExistError("entity metadata does not exist")
        os.remove(path=entity_metadata_path)
