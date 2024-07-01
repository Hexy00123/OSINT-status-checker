from fastapi import FastAPI
from src.routers import status
from src.lifespan import lifespan


app = FastAPI(lifespan=lifespan)
# app.include_router(task.router)
app.include_router(status.router)
