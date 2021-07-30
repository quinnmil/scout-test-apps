import logging.config
import os
import time
from types import SimpleNamespace

import celery
from celery.signals import setup_logging
import scout_apm.celery


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

# Imitate Django settings
app.config_from_object(
    SimpleNamespace(
        SCOUT_MONITOR=True,
        SCOUT_KEY=os.environ["SCOUT_KEY"],
        SCOUT_NAME="Test Celery App",
        SCOUT_ERRORS_ENABLED=True,
    ),
    namespace="CELERY_",
)


@app.task
def sleep(n):
    time.sleep(n)


@app.task
def crash(spam, foo=None):
    raise ValueError("Boom!")


scout_apm.celery.install(app)
