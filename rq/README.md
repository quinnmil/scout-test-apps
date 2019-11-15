RQ
==

For testing the [RQ](https://python-rq.org/) integration.

Setup
-----

**First,** run Redis with:

```
$ docker run --detach --name redis --publish 6379:6379 redis:5.0.4-alpine
```

**Second,** set up the local environment:

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

**Third,** run the worker with:

```
$ export SCOUT_KEY=your-key-here
$ rq worker --config app_config --worker-class scout_apm.rq.Worker
```

You should see startup logging from both RQ and Scout.

**Fourth,** start another terminal, activate the virtual environment, and open
IPython:

```
$ source venv/bin/activate
$ ipython
```

Here you can import and enqueue tasks as you wish to test:

```
In [1]: import app

In [2]: app.queue.enqueue(app.hello)
Out[2]: Job('51c87d5b-e8c7-4e3d-97d8-bff59f2c0a38', enqueued_at=datetime.datetime(2019, 11, 15, 15, 34, 11, 738685))
```

On the worker terminal tab, you should see RQ's logging that the task has run,
and Scout's logging around the request being tracked.
