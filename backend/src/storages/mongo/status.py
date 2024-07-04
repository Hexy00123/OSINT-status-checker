from datetime import datetime

from beanie import Document, TimeSeriesConfig
from pydantic import BaseModel

from src.storages.mongo.user import User


class Status(Document):
    ts: datetime
    username: str
    is_online: bool

    class Settings:
        timeseries = TimeSeriesConfig(
            time_field="ts",
            meta_field="user",
        )


class StatusCreate(BaseModel):
    ts: datetime
    username: str
    is_online: bool


class StatusRepository:
    async def create(self, obj: StatusCreate):
        status = Status(**obj.model_dump())
        return await status.insert()

    async def read_by(
        self, username: str = None, start: datetime = None, end: datetime = None
    ):
        criteria = []
        if username:
            criteria.append(Status.username == username)
        if start:
            criteria.append(Status.ts >= start)
        if end:
            criteria.append(Status.ts <= end)
        return await Status.find_many(*criteria).to_list()

    async def read_all(self):
        return await Status.find_many({}).to_list()


status_repository = StatusRepository()
