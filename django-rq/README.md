Django-RQ
=========

For testing the [RQ](https://python-rq.org/) integration running with
[django-rq](https://github.com/rq/django-rq).

Setup
-----

**First,** run Redis with:

```
$ docker run --detach --name redis --publish 6379:6379 redis:5.0.4-alpine
```

**Second,** set up your local environment:

```
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

*If* you want to test with a local, in-development version of `scout-apm`,
install that with:

```
$ pip install -e /path/to/scout_apm_python  # optional!
```

**Third,** run the RQ worker with:

```
$ export SCOUT_KEY=your-key-here
$ python app.py rqworker
```

You should see startup logging from both RQ and Scout.

**Fourth,** start another terminal, activate the virtual environment, and open
IPython via Django:

```
$ source venv/bin/activate
$ python app.py shell
```

Here you can import and enqueue tasks as you wish to test:

```
In [1]: import app, django_rq

In [2]: app.queue.enqueue(app.hello)
Out[2]: Job('ce4e7a6b-09a2-4bc0-87ce-ea46956e9d78', enqueued_at=datetime.datetime(2019, 11, 15, 17, 3, 14, 126720))
```

On the worker terminal tab, you should see RQ's logging that the task has run,
and Scout's logging around the request being tracked.
