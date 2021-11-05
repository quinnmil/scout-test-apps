import asyncio
import logging
import os

import uvicorn
from scout_apm.api import Config, instrument
from scout_apm.async_.starlette import ScoutMiddleware
from scout_apm.sqlalchemy import instrument_sqlalchemy
from fastapi import BackgroundTasks, FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, User, Base
from database_async import database, users, engine as async_engine

Base.metadata.create_all(bind=engine)
instrument_sqlalchemy(engine)
# instrument_sqlalchemy(async_engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.on_event("startup")
async def startup():
    await database.connect()


# @app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "stdout": {
                "format": "%(asctime)s %(levelname)s %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%S%z",
            }
        },
        "handlers": {
            "stdout": {"class": "logging.StreamHandler", "formatter": "stdout"}
        },
        "root": {"handlers": ["stdout"], "level": "DEBUG"},
    }
)


async def get_welcome():
    with instrument("get_welcome"):
        await asyncio.sleep(0.1)
        return "Welcome"


async def get_home():
    with instrument("get_home"):
        await asyncio.sleep(0.2)
        return "home"


@app.get("/")
async def home():
    return {
        "get_home": await get_home(),
        "get_welcome": await get_welcome(),
    }


@app.get("/sync")
def sync_home(db: Session = Depends(get_db)):
    from scout_apm.core.tracked_request import TrackedRequest

    print("sync", TrackedRequest.instance())
    x = []
    # for i in range(-100, 0):
    #    x.append(len(db.query(User).filter(User.id >= i).all()))
    return {"users": len(db.query(User).all())}


@app.get("/crash")
async def crash():
    raise ValueError("BØØM!")  # non-ASCII


def sync_task():
    print("Doing the sync task ! ✨")


async def async_task():
    print("Doing the async task ! 🎉")


@app.get("/background_jobs")
async def background_jobs(background_tasks: BackgroundTasks):
    background_tasks.add_task(sync_task)
    background_tasks.add_task(async_task)

    return {"message": "Triggering background jobs."}


@app.get("/await")
async def await_task(background_tasks: BackgroundTasks):
    async def awaiting_task():
        with instrument("awaiting_task"):
            await asyncio.sleep(0.1)
            return "done"

    task = asyncio.ensure_future(awaiting_task())
    await task
    return {"message": "Awaited task."}


async def error(request, exc):
    # Always raise exceptions, rather than convert them into pages
    raise exc


app.exception_handlers = {
    500: error,
}


# Installation instructions
Config.set(
    key=os.environ["SCOUT_KEY"],
    name="Test FastAPI App",
    monitor=True,
)
app.add_middleware(ScoutMiddleware)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
