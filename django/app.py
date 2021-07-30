import logging
import os
import random
import sys
import time

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.utils.html import escape

logging.getLogger().setLevel(logging.DEBUG)

settings.configure(
    DEBUG=(os.environ.get("DEBUG", "") == "1"),
    ALLOWED_HOSTS=["*"],  # Disable allowed host checking
    ROOT_URLCONF=__name__,  # Make this module the urlconf
    SECRET_KEY=get_random_string(50),
    BASE_DIR=os.path.dirname(os.path.abspath(__file__)),
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
    INSTALLED_APPS=["scout_apm.django", "django.contrib.sessions"],
    MIDDLEWARE=["django.contrib.sessions.middleware.SessionMiddleware"],
    SESSION_ENGINE="django.contrib.sessions.backends.file",
    SCOUT_MONITOR=True,
    SCOUT_KEY=os.environ["SCOUT_KEY"],
    SCOUT_NAME="Test Django App",
    SCOUT_IGNORE=["/ignore"],
    SCOUT_ERRORS_ENABLED=True
)


def index(request):
    name = request.GET.get("name", "World")
    if random.random() < 0.1:
        time.sleep(1)
    return HttpResponse("Hello, " + escape(name) + "!")


def session(request):
    session_key = 'session_value'
    value = int(request.session.get(session_key) or 0)
    request.session[session_key] = value + 1
    return HttpResponse("Updated session value to {}".format(request.session[session_key]))


def crash(request, foo):
    1 / 0
    return HttpResponse("Broken.")


def ignore(request):
    return HttpResponse("Ignore me!")


try:
    from django.urls import path

    urlpatterns = [
        path("", index),
        path("ignore/", ignore),
        path("session/", session),
        path("crash/<foo>/", crash),
    ]
except ImportError:
    # Django < 2.0
    from django.conf.urls import url

    urlpatterns = [
        url(r"^$", index),
        url(r"^ignore/$", ignore),
        url(r"^session/$", session),
        url(r"^crash/(?P<foo>\w+)/$", crash),
    ]

application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
