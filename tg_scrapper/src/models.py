from typing import Annotated, Literal

from beanie import Document, Indexed


class User(Document):
    username: Annotated[str, Indexed(unique=True)]
    app: Literal["tg", "vk"]
