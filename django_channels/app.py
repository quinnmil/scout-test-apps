import asyncio
import logging
import os
import random
import sys
import time

from channels.http import AsgiHandler
from channels.generic.http import AsyncHttpConsumer
from channels.routing import URLRouter
from django.conf import settings
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.utils.html import escape

logging.getLogger().setLevel(logging.DEBUG)

settings.configure(
    ASGI_APPLICATION="__main__.application",
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
    SCOUT_MONITOR=True,
    SCOUT_NAME="Test Django Channels App",
)


def index(request):
    name = request.GET.get("name", "World")
    if random.random() < 0.1:
        time.sleep(1)
    return HttpResponse("Hello, " + escape(name) + "!")


try:
    from django.urls import path

    urlpatterns = [path("", index)]
except ImportError:
    # Django < 2.0
    from django.conf.urls import url

    urlpatterns = [url(r"^$", index)]


class BasicHttpConsumer(AsyncHttpConsumer):
    async def handle(self, body):
        await asyncio.sleep(1)
        await self.send_response(
            200,
            b"Hello world, asynchronously!",
            headers=[(b"Content-Type", b"text/plain")],
        )


application = URLRouter([url(r"^async/$", BasicHttpConsumer), url(r"", AsgiHandler)])

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
