from datetime import datetime

from beanie import Document, TimeSeriesConfig
from pydantic import BaseModel


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

    async def read_all(self):
        return await Status.find_many({}).to_list()


status_repository = StatusRepository()
