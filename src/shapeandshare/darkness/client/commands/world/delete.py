import requests

from .... import Response
from ....sdk.contracts.dtos.sdk.requests.world.delete import WorldDeleteRequest
from ..abstract import AbstractCommand


class WorldDeleteCommand(AbstractCommand):
    async def execute(self, request: WorldDeleteRequest) -> bool:
        response: requests.Response = requests.delete(
            url=f"http://{self.options.tld}/world/{request.id}",
            timeout=self.options.timeout,
            params={"cascade": request.cascade},
        )
        return Response[bool].model_validate(response.json()).data
