import logging
import os
import random
import sys
import time


from django.conf import settings
from django.conf.urls import url
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.utils.html import escape

logging.getLogger().setLevel(logging.DEBUG)

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
                "format": "%(asctime)s %(levelname)s %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%S%z",
            }
        },
        "handlers": {
            "stdout": {"class": "logging.StreamHandler", "formatter": "stdout"}
        },
        "root": {"handlers": ["stdout"], "level": "DEBUG"},
    },
    INSTALLED_APPS=["channels", "scout_apm.django"],
    CHANNEL_LAYERS={
        "default": {
            "BACKEND": "asgiref.inmemory.ChannelLayer",
            "ROUTING": "__main__.channel_routing",
        }
    },
    SCOUT_MONITOR=True,
    SCOUT_NAME="Test Django Channels 1 App",
)


def index(request):
    name = request.GET.get("name", "World")
    if random.random() < 0.1:
        time.sleep(1)
    return HttpResponse("Hello, " + escape(name) + "!")


urlpatterns = [url(r"^$", index)]


channel_routing = []

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
