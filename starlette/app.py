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


async def get_welcome():
    with instrument("get_welcome"):
        await asyncio.sleep(0.1)
        return "Welcome"


async def get_home():
    with instrument("get_home"):
        await asyncio.sleep(0.2)
        return "home"


async def home(request):
    return PlainTextResponse(f"{await get_welcome()} {await get_home()}.")


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


async def await_task(request):

    async def awaiting_task():
        with instrument('awaiting_task'):
            await asyncio.sleep(0.1)
            return "done"

    task = asyncio.create_task(awaiting_task())
    await task
    return PlainTextResponse("Awaited task.")


async def error(request, exc):
    # Always raise exceptions, rather than convert them into pages
    raise exc


app = Starlette(
    routes=[
        Route("/", home),
        Route("/hello/", HelloEndpoint),
        Route("/crash/", crash),
        Route("/background-jobs/", background_jobs),
        Route("/await-task/", await_task),
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
