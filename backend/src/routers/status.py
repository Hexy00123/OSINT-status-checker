from fastapi import APIRouter

from backend.src.storages.mongo.status import Status

router = APIRouter(prefix="/status", tags=["Status"])


@router.post("/")
async def create(status: Status):
    pass
