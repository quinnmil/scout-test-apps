import logging
import os
import sys

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.urls import path
from django.utils.crypto import get_random_string

logging.getLogger().setLevel(logging.DEBUG)

settings.configure(
    ALLOWED_HOSTS=["*"],  # Disable allowed host checking
    DEBUG=(os.environ.get("DEBUG", "") == "1"),
    INSTALLED_APPS=["scout_apm.django", "rest_framework"],
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
            "stdout": {"class": "logging.StreamHandler", "formatter": "stdout"},
            "scout_apm": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": "scout_apm_debug.log",
            },
        },
        "root": {"handlers": ["stdout"], "level": os.environ.get("LOG_LEVEL", "DEBUG")},
        "loggers": {
            "scout_apm": {
                "handlers": ["scout_apm"],
                "level": "DEBUG",
                "propagate": True,
            }
        },
    },
    ROOT_URLCONF=__name__,  # Make this module the urlconf
    SECRET_KEY=get_random_string(50),
    # Django Rest Framework
    REST_FRAMEWORK={
        # Disable authentication against django.contrib.auth
        "DEFAULT_AUTHENTICATION_CLASSES": [],
        # Disable permissions checking against django.contrib.auth
        "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
        # Disable browsable API, and thus dependency on templates
        "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
        # Remove dependency on django.contrib.auth by not using AnonymousUser
        # for unauthenticated users but instead a plain old object
        "UNAUTHENTICATED_USER": "builtins.object",
    },
    # Scout
    SCOUT_MONITOR=True,
    SCOUT_KEY=os.environ["SCOUT_KEY"],
    SCOUT_NAME="Test Django+DRF App",
    SCOUT_IGNORE=["/ignore"],
)

# Can't import DRF bits until settings configured
from rest_framework.decorators import api_view  # noqa
from rest_framework.response import Response  # noqa
from rest_framework.routers import SimpleRouter  # noqa
from rest_framework.viewsets import ViewSet  # noqa


@api_view(["GET"])
def index(request):
    return Response({"message": "Hello, world!"})


class MyViewSet(ViewSet):
    """
    Simple queryset-less ViewSet to test router functionality
    """

    def list(self, request):
        return Response({"my": "viewset"})


router = SimpleRouter()
router.register("my", MyViewSet, basename="my")

urlpatterns = [path("", index)] + router.urls

app = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
