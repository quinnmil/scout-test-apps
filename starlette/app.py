import asyncio
import logging
import os

import uvicorn
from scout_apm.api import Config, instrument
from scout_apm.async_.starlette import ScoutMiddleware
from starlette.applications import Starlette
from starlette.background import BackgroundTasks
from starlette.endpoints import HTTPEndpoint
from starlette.responses import PlainTextResponse
from starlette.routing import Route

logging.config.dictConfig({
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
})


async def home(request):
    with instrument("sleep"):
        await asyncio.sleep(1)
    return PlainTextResponse("Welcome home.")


class HelloEndpoint(HTTPEndpoint):
    async def get(self, request):
        return PlainTextResponse("Hello World!")


async def crash(request):
    raise ValueError("BØØM!")  # non-ASCII


async def background_jobs(request):
    def sync_task():
        print("Doing the sync task ! ✨")

    async def async_task():
        print("Doing the async task ! 🎉")

    tasks = BackgroundTasks()
    tasks.add_task(sync_task)
    tasks.add_task(async_task)

    return PlainTextResponse("Triggering background jobs", background=tasks)


async def error(request, exc):
    # Always raise exceptions, rather than convert them into pages
    raise exc


app = Starlette(
    routes=[
        Route("/", home),
        Route("/hello/", HelloEndpoint),
        Route("/crash/", crash),
        Route("/background-jobs/", background_jobs),
    ],
    exception_handlers={
        500: error,
    }
)


# Installation instructions
Config.set(
    key=os.environ["SCOUT_KEY"],
    name="Test Starlette App",
    monitor=True,
)
app.add_middleware(ScoutMiddleware)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
