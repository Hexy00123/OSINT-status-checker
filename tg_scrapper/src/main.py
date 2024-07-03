from fastapi import FastAPI
from src.routers import status, user
from src.lifespan import lifespan


app = FastAPI(lifespan=lifespan)
app.include_router(user.router)
