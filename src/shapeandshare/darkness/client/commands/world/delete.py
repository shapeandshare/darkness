import requests

from ....sdk.contracts.dtos.sdk.requests.world.world import WorldRequest
from ..abstract import AbstractCommand


class WorldDeleteCommand(AbstractCommand):
    async def execute(self, request: WorldRequest) -> None:
        requests.delete(url=f"http://{self.options.tld}/world/{request.id}", timeout=self.options.timeout)
