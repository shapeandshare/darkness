from ..contracts.dtos.command_options import CommandOptions
from ..contracts.dtos.island import Island
from ..contracts.dtos.requests.island_create_request import IslandCreateRequest
from ..contracts.dtos.requests.island_get_request import IslandGetRequest
from ..contracts.dtos.responses.island_create_response import IslandCreateResponse
from ..contracts.dtos.responses.island_get_response import IslandGetResponse
from ..contracts.dtos.responses.islands_get_response import IslandsGetResponse
from ..contracts.types.tile import TileType
from .commands.island.island_create import IslandCreateCommand
from .commands.island.island_get import IslandGetCommand
from .commands.islands.islands_get import IslandsGetCommand
from .commands.metrics.health_get import HealthGetCommand


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

    def island_create(self, dim: tuple[int, int], biome: TileType) -> str:
        request: IslandCreateRequest = IslandCreateRequest(dim=dim, biome=biome)
        response: IslandCreateResponse = self.island_create_command.execute(request=request)
        return response.id

    def island_get(self, id: str) -> Island:
        request: IslandGetRequest = IslandGetRequest(id=id)
        response: IslandGetResponse = self.island_get_command.execute(request=request)
        return response.island

    def islands_get(self) -> list[str]:
        response: IslandsGetResponse = self.islands_get_command.execute()
        return response.ids
