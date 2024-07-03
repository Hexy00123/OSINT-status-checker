from typing import Annotated, Literal

from beanie import Document, Indexed, PydanticObjectId
from pydantic import BaseModel
from pymongo import IndexModel
import pymongo


class User(Document):
    username: str
    app: Literal["tg", "vk"]

    class Settings:
        indexes = [
            IndexModel(
                [("username", pymongo.ASCENDING), ("app", pymongo.ASCENDING)],
                unique=True,
            )
        ]


class UserCreate(BaseModel):
    username: str
    app: Literal["tg", "vk"]


class UserRepository:
    async def create(self, obj: UserCreate) -> User:
        user = User(**obj.model_dump())
        return await user.insert()

    async def create_many(self, objs: list[UserCreate]) -> list[str]:
        users = [User(**obj.model_dump()) for obj in objs]
        insert_many_result = await User.insert_many(users)
        return insert_many_result.inserted_ids

    async def read(self, id: str) -> User:
        return await User.find_one({"_id": PydanticObjectId(id)})

    async def read_all(self) -> list[User]:
        return await User.find_many().to_list()

    async def delete(self, id: str) -> User:
        user = await User.find_one({"_id": PydanticObjectId(id)})
        if user:
            await user.delete()
        return user


user_repository = UserRepository()
