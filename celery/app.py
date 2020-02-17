import logging.config
import os
import time

import celery
from celery.signals import setup_logging
import scout_apm.celery
from scout_apm.api import Config


@setup_logging.connect
def basic_logging_setup(**kwargs):
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


app = celery.Celery("app", broker="redis://localhost:6379/0")


@app.task
def sleep(n):
    time.sleep(n)


Config.set(
    monitor=True,
    key=os.environ["SCOUT_KEY"],
    name="Test Celery App",
)
scout_apm.celery.install()
