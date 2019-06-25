import os

import falcon

from scout_apm.falcon import ScoutMiddleware

scout_middleware = ScoutMiddleware(config={
    "key": os.environ["SCOUT_KEY"],
    "monitor": True,
    "name": "Test Falcon App",
})
api = falcon.API(middleware=[scout_middleware])
scout_middleware.set_api(api)


class HomeResource(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_TEXT
        resp.body = "Welcome home."

    def on_get_suffixed(self, req, resp):
        self.on_get(req, resp)
        resp.body = "Welcome home, suffixed."


api.add_route("/", HomeResource())
api.add_route("/suffixed", HomeResource(), suffix="suffixed")


class CrashResource(object):
    def on_get(self, req, resp):
        raise falcon.HTTPStatus("748 Confounded by ponies")


api.add_route("/crash", CrashResource())
