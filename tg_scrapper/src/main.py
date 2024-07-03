from fastapi import FastAPI
from src.routers import user, qr
from src.lifespan import lifespan


app = FastAPI(lifespan=lifespan)
app.include_router(user.router)
app.include_router(qr.router)
