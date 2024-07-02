from datetime import datetime

from beanie import Document, Link, PydanticObjectId, TimeSeriesConfig
from bson import DBRef
from pydantic import BaseModel, field_validator

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


class StatusCreate(BaseModel):
    ts: datetime
    user: Link[User]
    is_online: bool

    # @field_validator("user")
    # def validate_user(cls, v: str):
    #     return Link(DBRef("User", PydanticObjectId(v)), User)


class StatusRepository:
    async def create(self, obj: StatusCreate):
        status = Status(**obj.model_dump())
        return await status.insert()

    async def read_all(self):
        return await Status.find_many({}).to_list()


status_repository = StatusRepository()
