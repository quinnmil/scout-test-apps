"""
Run redis with `docker run --name dramatiq-redis -p 6379:6379 redis:5.0.4-alpine`

Run as a worker with `dramatiq app`

Run `ipython`, `import app`, and run e.g. `sleep.send(n)`
"""
import os
import time

import dramatiq
from dramatiq.brokers.redis import RedisBroker
from scout_apm.api import Config
from scout_apm.dramatiq import ScoutMiddleware


broker = RedisBroker()
broker.add_middleware(ScoutMiddleware(), before=broker.middleware[0].__class__)
dramatiq.set_broker(broker)

Config.set(
    key=os.environ["SCOUT_KEY"],
    name="Test Dramatiq App",
    monitor=True,
)


@dramatiq.actor(max_retries=0)
def sleep(n):
    time.sleep(n)


@dramatiq.actor(max_retries=0)
def fail():
    raise ValueError()
