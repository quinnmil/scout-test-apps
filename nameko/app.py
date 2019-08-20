# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import os

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
