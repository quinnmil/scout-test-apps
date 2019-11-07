"""
Run with:
    huey_consumer.py app.huey

And then add tasks in `ipython` with:

    import app
    result = app.hello()
    result(blocking=True)

"""
import logging.config

from huey import SqliteHuey
from scout_apm.api import Config
from scout_apm.huey import attach_scout

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

huey = SqliteHuey(filename="db.sqlite3")


@huey.task()
@huey.lock_task("hello")
def hello():
    return "Hello World!"


@huey.task()
def fail():
    raise ValueError("BØØM!")  # non-ASCII


# Setup according to https://docs.scoutapm.com/#huey
Config.set(
    name="Test Huey App",
    monitor=True,
)
attach_scout(huey)
