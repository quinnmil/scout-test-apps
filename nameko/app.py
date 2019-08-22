# coding=utf-8
"""
To start:
1. docker run -d --name rabbitmq -p 5672:5672 rabbitmq:3.7.17
2. nameko run app

Then can invoke the service with either:
1. http://localhost:8000/
2. nameko shell
   >>> n.rpc.myservice.hello("me")
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import os

from nameko.rpc import rpc
from nameko.web.handlers import http

from scout_apm.api import Config
from scout_apm.nameko import ScoutReporter


Config.set(
    key=os.environ["SCOUT_KEY"],
    name="Test Nameko App",
    monitor=True,
)


class Service(object):
    name = "myservice"

    scout = ScoutReporter()

    @http("GET", "/")
    def home(self, request):
        return "Welcome home."

    @http("GET", "/crash/")
    def crash(self, request):
        raise ValueError("BØØM!")  # non-ASCII

    @rpc
    def hello(self, name):
        return "Hello, {}!".format(name)
