import logging.config
import os

import cherrypy

from scout_apm.api import Config
from scout_apm.cherrypy import ScoutPlugin


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


class Views(object):
    @cherrypy.expose
    def index(self, **params):
        return "Welcome home."

    @cherrypy.expose
    def hello(self, name="World"):
        return f"Hello {name}!"

    @cherrypy.expose
    def crash(self):
        raise ValueError("BØØM!")

    @cherrypy.expose
    def return_error(self):
        cherrypy.response.status = 503
        return "Something went wrong"


app = cherrypy.Application(Views(), "/", config=None)


# https://docs.scoutapm.com/#cherrypy
Config.set(
    monitor=True,
    key=os.environ["SCOUT_KEY"],
    name="Test CherryPy App",
)
plugin = ScoutPlugin(cherrypy.engine)
plugin.subscribe()


if __name__ == '__main__':
    cherrypy.quickstart(Views())
