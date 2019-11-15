import os
import sys

from django.conf import settings
from django.utils.crypto import get_random_string

if not settings.configured:
    settings.configure(
        DEBUG=(os.environ.get("DEBUG", "") == "1"),
        ALLOWED_HOSTS=["*"],  # Disable allowed host checking
        ROOT_URLCONF=__name__,  # Make this module the urlconf
        SECRET_KEY=get_random_string(50),
        LOGGING={
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "stdout": {
                    "format": "%(asctime)s %(levelname)s\t%(name)s %(message)s",
                    "datefmt": "%Y-%m-%dT%H:%M:%S%z",
                }
            },
            "handlers": {
                "stdout": {"class": "logging.StreamHandler", "formatter": "stdout"}
            },
            "root": {"handlers": ["stdout"], "level": "DEBUG"},
        },
        INSTALLED_APPS=["scout_apm.django", "django_rq"],
        SCOUT_MONITOR=True,
        SCOUT_NAME="Test Django-RQ App",
        RQ={"WORKER_CLASS": "scout_apm.rq.Worker"},
        RQ_QUEUES={
            'default': {
                'HOST': 'localhost',
                'PORT': 6379,
                'DB': 0,
            },
        }
    )

urlpatterns = []


def hello():
    return "Hello World!"


def fail():
    raise ValueError("BØØM!")  # non-ASCII


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
