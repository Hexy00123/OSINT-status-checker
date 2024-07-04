from fastapi import APIRouter, HTTPException
from pymongo.errors import DuplicateKeyError

from src.storages.mongo.user import User, UserCreate, user_repository

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/")
async def create(obj: UserCreate) -> User:
    try:
        user = await user_repository.create(obj)
    except DuplicateKeyError:
        raise HTTPException(status_code=409)
    return user


@router.post("/create-many")
async def create_many(objs: list[UserCreate]) -> list[str]:
    user_ids = []
    for obj in objs:
        try:
            user = await user_repository.create(obj)
            user_ids.append(str(user.id))
        except DuplicateKeyError:
            pass
    return user_ids


@router.get("/")
async def read_all() -> list[User]:
    return await user_repository.read_all()


# @router.delete("/")
# async def delete(id: str) -> User:
#     user = await user_repository.delete(id)
#     if not user:
#         raise HTTPException(status_code=404)
#     return user
