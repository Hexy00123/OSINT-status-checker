from datetime import datetime

from beanie import Document, Link, TimeSeriesConfig

from src.storages.mongo.user import User


class Status(Document):
    ts: datetime
    user: Link[User]
    is_online: bool

    class Settings:
        timeseries = TimeSeriesConfig(
            time_field="ts",
            meta_field="user",
        )


class StatusRepository:
    async def create(self, status: Status):
        return await status.create()


status_repository = StatusRepository()
