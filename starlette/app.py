import logging
import os

import uvicorn
from scout_apm.api import Config
from scout_apm.async_.starlette import ScoutMiddleware
from starlette.applications import Starlette
from starlette.background import BackgroundTasks
from starlette.endpoints import HTTPEndpoint
from starlette.responses import PlainTextResponse

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

app = Starlette()


@app.route("/")
async def home(request):
    return PlainTextResponse("Welcome home.")


@app.route("/hello/")
class HelloEndpoint(HTTPEndpoint):
    async def get(self, request):
        return PlainTextResponse("Hello World!")


@app.route("/crash/")
async def crash(request):
    raise ValueError("BØØM!")  # non-ASCII


@app.route("/background-jobs/")
async def background_jobs(request):
    def sync_task():
        print("Doing the sync task ! ✨")

    async def async_task():
        print("Doing the async task ! 🎉")

    tasks = BackgroundTasks()
    tasks.add_task(sync_task)
    tasks.add_task(async_task)

    return PlainTextResponse("Triggering background jobs", background=tasks)


@app.exception_handler(500)
async def error(request, exc):
    # Always raise exceptions
    raise exc

# Installation instructions
Config.set(
    key=os.environ["SCOUT_KEY"],
    name="Test Starlette App",
    monitor=True,
)
app.add_middleware(ScoutMiddleware)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
