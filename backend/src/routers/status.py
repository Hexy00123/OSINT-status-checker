from fastapi import APIRouter

from src.storages.mongo.status import Status, status_repository

router = APIRouter(prefix="/status", tags=["Status"])


@router.post("/")
async def create(obj: Status):
    return await Status.insert(obj)


@router.post("/create-many")
async def create_many(objs: list[Status]):
    insert_many_result = await Status.insert_many(objs)
    return insert_many_result.inserted_ids 
