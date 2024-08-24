import requests

from ....sdk.contracts.dtos.sdk.responses.response import Response
from ....sdk.contracts.dtos.sdk.responses.worlds.get import WorldsGetResponse
from ....sdk.contracts.dtos.tiles.world import World
from ..abstract import AbstractCommand


class WorldsGetCommand(AbstractCommand):
    async def execute(self) -> WorldsGetResponse:
        response: requests.Response = requests.get(
            url=f"http://{self.options.tld}/worlds", timeout=self.options.timeout
        )
        return Response[WorldsGetResponse].model_validate(response.json()).data
