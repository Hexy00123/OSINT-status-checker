from datetime import datetime

from beanie import Document, Field, Link, TimeSeriesConfig

from src.storages.mongo.user import User


class Status(Document):
    ts: datetime = Field(default_factory=datetime.now)
    user: Link[User]
    is_online: bool

    class Settings:
        timeseries = TimeSeriesConfig(
            time_field="ts",
            meta_field="user",
        )


class StatusRepository:
    async def create():
        pass
