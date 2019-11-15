import os
import time

from redis import Redis
from rq import Queue
from scout_apm.api import Config


def hello():
    return "Hello World!"


def fail():
    raise ValueError("BØØM!")  # non-ASCII


queue = Queue(connection=Redis())
