from typing import Literal

from pydantic import BaseModel

class User(BaseModel):
    username: str
    app: Literal["tg", "vk"]
