from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

from src.scrapper import scrapper_initialization, scrapper_run

USERS = []

async def lifespan(app: FastAPI):
    global USERS

    scheduler = BackgroundScheduler(job_defaults={'max_instances': 10})

    driver, wait, USERS = scrapper_initialization()
    scheduler.add_job(scrapper_run, "interval", seconds=10, args=[driver, wait, USERS])
    scheduler.start()
    yield
