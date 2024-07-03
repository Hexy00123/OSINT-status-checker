from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

from src.scrapper import scrapper_initialization, scrapper_run

USERS = []

async def lifespan(app: FastAPI):
    global USERS

    scheduler = BackgroundScheduler()

    driver, USERS = scrapper_initialization()
    scheduler.add_job(scrapper_run, "interval", seconds=10, args=[driver, USERS])
    scheduler.start()
    yield
