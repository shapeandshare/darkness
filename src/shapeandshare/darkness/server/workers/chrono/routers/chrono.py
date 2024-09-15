import asyncio
import logging
from asyncio import Queue

from fastapi import APIRouter
from fastapi_utils.tasks import repeat_every

from ..... import demand_env_var_as_int, get_env_var
from .....sdk.contracts.dtos.tiles.world import World
from .....sdk.contracts.types.chunk_quantum import ChunkQuantumType
from ....api.common.middleware.error import error_handler
from ..context import ContextManager

logger = logging.getLogger()

router: APIRouter = APIRouter(
    prefix="/chrono",
    tags=["chrono"],
)


@repeat_every(
    seconds=(
        demand_env_var_as_int(name="DARKNESS_WORKER_CHRONO_SLEEP_TIME")
        if get_env_var(name="DARKNESS_WORKER_CHRONO_SLEEP_TIME")
        else 10
    )
)
async def world_chrono():
    logger.debug("world chrono process executing")
    if ContextManager.client is None:
        logger.warning("Chrono client is not yet initialized")
        return

    async def producer_chunk(queue: Queue):
        worlds: list[World] = await ContextManager.client.worlds_get()
        for world in worlds:
            for chunk_id in world.ids:
                await queue.put({"world_id": world.id, "chunk_id": chunk_id})

    async def step_one():
        async def consumer(queue: Queue):
            while not queue.empty():
                address_dict: dict = await queue.get()
                await ContextManager.client.chunk_quantum(
                    world_id=address_dict["world_id"], chunk_id=address_dict["chunk_id"], scope=ChunkQuantumType.ALL
                )
                queue.task_done()

        queue = asyncio.Queue()
        await asyncio.gather(producer_chunk(queue), consumer(queue))

    await step_one()


@router.post("")
@error_handler
async def chunk_quantum() -> None:
    await world_chrono()
