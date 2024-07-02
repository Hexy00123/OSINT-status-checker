from fastapi import APIRouter

from src.storages.mongo.status import Status, StatusCreate, status_repository

router = APIRouter(prefix="/status", tags=["Status"])


@router.post("/")
async def create(obj: StatusCreate):
    return await status_repository.create(obj)


@router.post("/create-many")
async def create_many(objs: list[Status]):
    insert_many_result = await Status.insert_many(objs)
    return list(map(str, insert_many_result.inserted_ids))


@router.get("/")
async def read_all() -> list[Status]:
    return await status_repository.read_all()
