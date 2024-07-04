from fastapi import APIRouter, HTTPException

from src.lifespan import USERS
from src.models import User

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/update")
async def update(obj: User):
    for user in USERS:
        if user["username"] == obj.username:
            raise HTTPException(status_code=422, detail="Duplicated user")
    USERS.append({"username": obj.username, "app": obj.app})
    print(USERS)
    return

@router.post("/update-many")
async def update_many(objs: list[User]):
    for obj in objs:
        for user in USERS:
            if user["username"] == obj.username:
                print(f"Skip user {obj.username} due to duplicate.")
        USERS.append({"username": obj.username, "app": obj.app})
    print(USERS)
    return
