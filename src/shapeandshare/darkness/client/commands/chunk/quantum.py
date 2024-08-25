import requests

from ....sdk.contracts.dtos.sdk.requests.chunk.quantum import ChunkQuantumRequest
from ..abstract import AbstractCommand


class ChunkQuantumCommand(AbstractCommand):
    async def execute(self, request: ChunkQuantumRequest) -> None:
        requests.post(
            url=f"http://{self.options.tld}/world/{request.world_id}/chunk/{request.chunk_id}",
            timeout=self.options.timeout,
            json=request.model_dump(exclude={"world_id", "chunk_id"}),
        )
