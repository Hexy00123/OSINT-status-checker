from fastapi import APIRouter

from src.lifespan import USERS
from src.models import User

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/update")
async def create(obj: User):
    USERS.append(obj)
    return
