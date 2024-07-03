from typing import Annotated, Literal

from beanie import Document, Indexed, PydanticObjectId
from pydantic import BaseModel


class User(Document):
    username: Annotated[str, Indexed(unique=True)]
    app: Literal["tg", "vk"]


class UserCreate(BaseModel):
    username: str
    app: Literal["tg", "vk"]


class UserRepository:
    async def create(self, obj: UserCreate):
        user = User(**obj.model_dump())
        return await user.insert()
    
    async def create_many(self, objs: list[UserCreate]):
        users = [User(**obj.model_dump()) for obj in objs]
        insert_many_result = await User.insert_many(users)
        return insert_many_result.inserted_ids
    
    async def read_all(self):
        return await User.find_many().to_list()

    async def delete(self, id: str):
        user = await User.find_one({"_id": PydanticObjectId(id)})
        delete_result = User.delete(user)
        return user


user_repository = UserRepository()
