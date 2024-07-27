# from fastapi import APIRouter, HTTPException
# from ..context import context
# from ...contracts.dtos.island import Island
#
# router: APIRouter = APIRouter(
#     prefix="/island",
#     tags=["island"],
#     responses={404: {"description": "Not found"}},
# )
#
# @router.get("/{island_id}")
# async def get_island(island_id: str):
#     print(f"[get_island] island_service is {type(context.island_service)}")
#     island: Island | None = context.island_service.get(id=island_id)
#     if island:
#         return {"data": island.model_dump()}
#     raise HTTPException(status_code=404, detail="Item not found")
