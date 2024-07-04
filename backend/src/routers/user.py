import requests
from fastapi import APIRouter, HTTPException
from pymongo.errors import DuplicateKeyError

from src.storages.mongo.user import User, UserCreate, user_repository

SCRAPPER_URL = "http://tg_scrapper:8000"

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/")
async def create(obj: UserCreate) -> User:
    try:
        user = await user_repository.create(obj)
        response = requests.post(f"{SCRAPPER_URL}/user/update", json={"app": obj.app, "username": obj.username})
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail=f'Failed to update user in tg scrapper: {response.json()}')
    except DuplicateKeyError:
        raise HTTPException(status_code=409)
    return user


@router.post("/create-many")
async def create_many(objs: list[UserCreate]) -> list[str]:
    user_ids = []
    users_to_update = []
    for obj in objs:
        try:
            user = await user_repository.create(obj)
            users_to_update.append({"username": obj.username, "app": obj.app})
            user_ids.append(str(user.id))
        except DuplicateKeyError:
            pass

    response = requests.post(f"{SCRAPPER_URL}/user/update-many", json=users_to_update)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail=f'Failed to update users in tg scrapper: {response.json()}')
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
