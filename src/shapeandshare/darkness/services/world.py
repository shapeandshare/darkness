import json
import logging
from pathlib import Path

from ..contracts.dtos.island import Island
from ..contracts.dtos.requests.island_create_request import IslandCreateRequest
from ..contracts.dtos.world import World
from ..contracts.errors.service import ServiceError
from ..factories.world.world import WorldFactory

logger = logging.getLogger()

STORAGE_BASE_PATH: Path = Path(".") / "data"
METADATA_PATH: Path = STORAGE_BASE_PATH / "metadata.json"


class WorldService:
    world: World | None = None
    # islands: dict[str, Island] = {}

    # # island_ids
    # islands: dict[str, str] = {}

    def __init__(self):
        STORAGE_BASE_PATH.mkdir(parents=True, exist_ok=True)

        if not METADATA_PATH.exists():
            self._generate()
            self._commit()
        else:
            self._read()

    ### Internal ##################################

    def _generate(self):
        logger.debug("[WorldService] generating world skeleton")
        self.world = WorldFactory.generate()

    def _read(self) -> None:
        logger.debug("[WorldService] loading world data from storage")
        try:
            if self.world:
                del self.world
                self.world = None
            self.world = World.parse_file(path=METADATA_PATH)
        except json.decoder.JSONDecodeError as error:
            error_message: str = f"[WorldService] Unable to load world data from ({METADATA_PATH})"
            logger.error(error_message)
            raise ServiceError(error_message) from error

    def _commit(self):
        logger.debug("[WorldService] writing world data to storage")
        world_data: str = self.world.model_dump_json(indent=4)
        with open(file=METADATA_PATH.resolve().as_posix(), mode="w", encoding="utf-8") as file:
            file.write(world_data)

    ### Islands ##################################

    def island_create(self, request: IslandCreateRequest) -> str:
        logger.debug("[WorldService] creating island")
        # discover an island and return its id.
        island_id: str = WorldFactory.island_discover(target_world=self.world, dim=request.dim, biome=request.biome)
        self._commit()
        return island_id

    def island_delete(self, id: str) -> None:
        msg: str = f"[WorldService] deleting island {id}"
        logger.debug(msg)
        if id in self.world.islands:
            del self.world.islands[id]
        self._commit()

    def island_get(self, id: str) -> Island:
        msg: str = f"[WorldService] getting island {id}"
        logger.debug(msg)

        try:
            island: Island = self.world.islands[id]
        except KeyError as error:
            msg: str = f"Unable to find island {id}"
            logger.error(msg)
            raise ServiceError(msg) from error
        return island

    def island_put(self, island: Island) -> None:
        msg: str = f"[WorldService] putting island {island.id} into world storage"
        logger.debug(msg)
        self.world.islands[island.id] = island
        self._commit()
