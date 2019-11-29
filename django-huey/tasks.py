from huey import SqliteHuey
from scout_apm.huey import attach_scout

huey = SqliteHuey(filename="db.sqlite3")
# Setup according to https://docs.scoutapm.com/#huey
# Settings done through Django
attach_scout(huey)


@huey.task()
@huey.lock_task("hello")
def hello():
    return "Hello World!"


@huey.task()
def fail():
    raise ValueError("BØØM!")  # non-ASCII
