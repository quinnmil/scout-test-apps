import asyncio
import os
import sys

from channels.http import AsgiHandler
from channels.generic.http import AsyncHttpConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.routing import URLRouter
from django.conf import settings
from django.http import HttpResponse
from django.utils.crypto import get_random_string

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
                "format": "%(asctime)s %(levelname)s\t%(name)s %(message)s",
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
    SCOUT_NAME="Test Django Channels 2 App",
)


def index(request):
    return HttpResponse(
        """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Django Channels 2 Test App</title>
        </head>
        <body>
            <p><a href="/sse/">Server Sent Events Test Page</a></p>
            <p><a href="/ws/">Websockets Test Page</a></p>
        </body>
        """
    )


class ServerSentEventsPage(AsyncHttpConsumer):
    """
    Implemented as a pretty basic Channels AsyncHTTPConsumer to test that.
    """
    async def handle(self, body):
        await self.send_headers(
            headers=[(b"Content-Type", b"text/html")]
        )
        await self.send_body(
            b"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Server Sent Events Page</title>
                <meta charset="UTF-8">
            </head>
            <body>
                <script>
                    const eventSource = new EventSource("/sse-source/");
                    eventSource.onmessage = function(event) {
                        const newElement = document.createElement("p");
                        newElement.innerHTML = event.data;
                        document.getElementsByTagName("body")[0].appendChild(newElement);
                    }
                </script>
            </body>
            </html>
            """
        )


class ServerSentEventsSource(AsyncHttpConsumer):
    """
    Implemented as a more complicated AsyncHttpConsumer to test that our traces
    can capture long pauses.
    """
    async def handle(self, body):
        await self.send_headers(
            headers=[
                (b"Cache-Control", b"no-cache"),
                (b"Content-Type", b"text/event-stream"),
                (b"Transfer-Encoding", b"chunked"),
            ]
        )
        messages = [
            "Hello!",
            "This page...",
            "...will load...",
            "...one chunk...",
            "...at a time.",
            "This is...",
            "...because it's using...",
            "...server sent events.",
        ]
        for message in messages:
            await asyncio.sleep(1.0)
            await self.send_body(f"data: {message}\n\n".encode("utf-8"), more_body=True)
        await self.send_body(b"")


class WebsocketsPage(AsyncHttpConsumer):
    async def handle(self, body):
        await self.send_headers(
            headers=[(b"Content-Type", b"text/html")]
        )
        await self.send_body(
            b"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Websockets Page</title>
                <meta charset="UTF-8">
            </head>
            <body>
                <script>
                    const chatSocket = new WebSocket('ws://' + window.location.host + '/ws-source/');

                    chatSocket.onmessage = function(event) {
                        const newElement = document.createElement("p");
                        newElement.innerHTML = event.data;
                        document.getElementsByTagName("body")[0].appendChild(newElement);
                    };

                    chatSocket.onclose = function() {
                        const newElement = document.createElement("p");
                        newElement.textContent = "Connection closed";
                        document.getElementsByTagName("body")[0].appendChild(newElement);
                    };
                </script>
            </body>
            </html>
            """
        )


class WebsocketsSource(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        messages = [
            "Hello there!",
            "This page...",
            "...will load...",
            "...one chunk...",
            "...at a time.",
            "This is...",
            "...because it's using...",
            "...websockets.",
        ]
        for message in messages:
            await asyncio.sleep(1.0)
            await self.send(text_data=message)

    async def disconnect(self, close_code):
        print("Client went away :(")


try:
    from django.urls import path

    urlpatterns = [path("", index)]
    application = URLRouter(
        [
            path("sse/", ServerSentEventsPage),
            path("sse-source/", ServerSentEventsSource),
            path("ws/", WebsocketsPage),
            path("ws-source/", WebsocketsSource),
            path("", AsgiHandler),
        ]
    )
except ImportError:
    # Django < 2.0
    from django.conf.urls import url

    urlpatterns = [url(r"^$", index)]
    application = URLRouter(
        [url(r"^async/$", AsyncHttpConsumer), url(r"", AsgiHandler)]
    )


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
