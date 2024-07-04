from datetime import datetime

from fastapi import APIRouter, HTTPException
from pymongo.errors import DuplicateKeyError

from src.storages.mongo.status import Status, StatusCreate, status_repository

router = APIRouter(prefix="/status", tags=["Status"])


@router.post("/")
async def create(obj: StatusCreate) -> Status:
    try:
        status = await status_repository.create(obj)
    except DuplicateKeyError:
        raise HTTPException(status_code=409)
    return status


@router.post("/create-many")
async def create_many(objs: list[StatusCreate]) -> list[str]:
    status_ids = []
    for obj in objs:
        try:
            status = await status_repository.create(obj)
            status_ids.append(str(status.id))
        except DuplicateKeyError:
            pass
    return status_ids


@router.get("/read-by")
async def read_by(
    username: str | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
) -> list[Status]:
    return await status_repository.read_by(username, start, end)


@router.get("/")
async def read_all() -> list[Status]:
    return await status_repository.read_all()
