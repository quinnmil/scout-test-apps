import logging.config
import os

import hug

from scout_apm.hug import integrate_scout


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


@hug.get("/")
def home():
    return "Welcome home."


@hug.get("/hello")
def hello(name="world"):
    return f"Hello {name}!"


integrate_scout(
    __name__,
    config={"key": os.environ["SCOUT_KEY"], "monitor": True, "name": "Test Hug App"},
)
