from ..sdk.contracts.dtos.island import Island
from ..sdk.contracts.dtos.sdk.command_options import CommandOptions
from ..sdk.contracts.dtos.sdk.requests.island.create import IslandCreateRequest
from ..sdk.contracts.dtos.sdk.requests.island.get import IslandGetRequest
from ..sdk.contracts.dtos.sdk.responses.island.create import IslandCreateResponse
from ..sdk.contracts.dtos.sdk.responses.island.get import IslandGetResponse
from ..sdk.contracts.dtos.sdk.responses.islands.get import IslandsGetResponse
from ..sdk.contracts.types.tile import TileType
from .commands.island.create import IslandCreateCommand
from .commands.island.get import IslandGetCommand
from .commands.metrics.health.get import HealthGetCommand
from .commands.world.get import IslandsGetCommand


class Client:
    health_get_command: HealthGetCommand

    island_create_command: IslandCreateCommand
    island_get_command: IslandGetCommand
    islands_get_command: IslandsGetCommand

    def __init__(self, options: CommandOptions | None = None):
        command_dict: dict = {}
        if options:
            command_dict["options"] = options

        ### Metrics
        self.health_get_command = HealthGetCommand.model_validate(command_dict)

        ### /island
        self.island_create_command = IslandCreateCommand.model_validate(command_dict)
        self.island_get_command = IslandGetCommand.model_validate(command_dict)

        ### /islands
        self.islands_get_command = IslandsGetCommand.model_validate(command_dict)

    def health_get(self) -> dict:
        """
        Gets the server health.

        Returns
        -------
        health: dict
            The server health (true or false).
        """

        return self.health_get_command.execute()

    def island_create(self, dimensions: tuple[int, int], biome: TileType) -> str:
        request: IslandCreateRequest = IslandCreateRequest(dimensions=dimensions, biome=biome)
        response: IslandCreateResponse = self.island_create_command.execute(request=request)
        return response.id

    def island_get(self, id: str) -> Island:
        request: IslandGetRequest = IslandGetRequest(id=id)
        response: IslandGetResponse = self.island_get_command.execute(request=request)
        return response.island

    def islands_get(self) -> list[str]:
        response: IslandsGetResponse = self.islands_get_command.execute()
        return response.ids
