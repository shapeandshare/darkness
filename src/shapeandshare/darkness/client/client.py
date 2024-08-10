from ..sdk.contracts.dtos.island import Island
from ..sdk.contracts.dtos.island_lite import IslandLite
from ..sdk.contracts.dtos.sdk.command_options import CommandOptions
from ..sdk.contracts.dtos.sdk.requests.island.create import IslandCreateRequest
from ..sdk.contracts.dtos.sdk.requests.island.get import IslandGetRequest
from ..sdk.contracts.dtos.sdk.responses.island.create import IslandCreateResponse
from ..sdk.contracts.dtos.sdk.responses.island.get import IslandGetResponse
from ..sdk.contracts.dtos.sdk.responses.islands.get import IslandsGetResponse
from ..sdk.contracts.types.tile import TileType
from .commands.island.create import IslandCreateCommand
from .commands.island.delete import IslandDeleteCommand
from .commands.island.get import IslandGetCommand
from .commands.metrics.health.get import HealthGetCommand
from .commands.world.create import WorldCreateCommand
from .commands.world.delete import WorldDeleteCommand
from .commands.world.get import IslandsGetCommand, WorldGetCommand


class Client:
    # metrics/health
    health_get_command: HealthGetCommand

    # island
    island_create_command: IslandCreateCommand
    island_delete_command: IslandDeleteCommand
    island_get_command: IslandGetCommand

    # world
    world_create_command: WorldCreateCommand
    world_get_command: WorldGetCommand
    world_delete_command: WorldDeleteCommand

    def __init__(self, options: CommandOptions | None = None):
        command_dict: dict = {}
        if options:
            command_dict["options"] = options

        ### metrics
        self.health_get_command = HealthGetCommand.model_validate(command_dict)

        ### island
        self.island_create_command = IslandCreateCommand.model_validate(command_dict)
        self.island_delete_command = IslandDeleteCommand.model_validate(command_dict)
        self.island_get_command = IslandGetCommand.model_validate(command_dict)

        # world
        self.world_create_command = WorldCreateCommand.model_validate(command_dict)
        self.world_get_command = WorldGetCommand.model_validate(command_dict)
        self.world_delete_command = WorldDeleteCommand.model_validate(command_dict)

    def health_get(self) -> dict:
        """
        Gets the server health.

        Returns
        -------
        health: dict
            The server health (true or false).
        """

        return self.health_get_command.execute()

    def island_create(self, world_id: str, name: str | None, dimensions: tuple[int, int], biome: TileType) -> str:
        request: IslandCreateRequest = IslandCreateRequest(
            world_id=world_id, name=name, dimensions=dimensions, biome=biome
        )
        response: IslandCreateResponse = self.island_create_command.execute(request=request)
        return response.id

    def island_get(self, world_id: str, island_id: str, full: bool = False) -> Island | IslandLite:
        request: IslandGetRequest = IslandGetRequest(world_id=world_id, island_id=island_id, full=full)
        response: IslandGetResponse = self.island_get_command.execute(request=request)
        return response.island

    # def islands_get(self) -> list[str]:
    #     response: IslandsGetResponse = self.islands_get_command.execute()
    #     return response.ids
