from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from src.storages.mongo.user import User
from src.storages.mongo.status import Status
import os

mongo_host = os.environ["MONGO_HOST"]


async def lifespan(app: FastAPI):
    motor_client = AsyncIOMotorClient(mongo_host)
    database = motor_client.get_database("osint_status_checker")
    await init_beanie(database=database, document_models=[User, Status])
    yield

    motor_client.close()