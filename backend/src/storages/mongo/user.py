from typing import Annotated, Literal

from beanie import Document, Indexed


class User(Document):
    id: str
    url: Annotated[str, Indexed(unique=True)]
    app: Literal["tg", "vk"]
