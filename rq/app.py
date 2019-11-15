from redis import Redis
from rq import Queue


def hello():
    return "Hello World!"


def fail():
    raise ValueError("BØØM!")  # non-ASCII


queue = Queue(connection=Redis())
