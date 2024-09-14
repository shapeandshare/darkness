import requests

from ....sdk.contracts.dtos.sdk.requests.world.delete import WorldDeleteRequest
from ....sdk.contracts.dtos.sdk.responses.response import Response
from ..abstract import AbstractCommand


class WorldDeleteCommand(AbstractCommand):
    async def execute(self, request: WorldDeleteRequest) -> bool:
        response: requests.Response = requests.delete(
            url=f"http://{self.options.tld}/world/{request.id}",
            timeout=self.options.timeout,
            params={"cascade": request.cascade},
        )
        return Response[bool].model_validate(response.json()).data
