from fastapi import APIRouter

from src.storages.mongo.user import User, UserCreate, user_repository

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/")
async def create(obj: UserCreate) -> User:
    return await user_repository.create(obj)


@router.post("create-many/")
async def create_many(objs: list[UserCreate]) -> list[str]:
    return await user_repository.create_many(objs)


@router.get("/")
async def read_all() -> list[User]:
    return await user_repository.read_all()


@router.delete("/")
async def delete(id: str):
    return await user_repository.delete(id)
