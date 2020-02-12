Celery
======

For testing the [Celery](https://docs.celeryproject.org/) integration.

Setup
-----

**First,** run Redis with:

```
$ docker run --detach --name redis --publish 6379:6379 redis:5
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
$ celery worker --app app
```

You should see startup logging from both Celery and Scout.

**Fourth,** start another terminal, activate the virtual environment, and open
IPython:

```
$ source venv/bin/activate
$ export SCOUT_KEY=your-key-here
$ ipython
```

Here you can import and enqueue tasks as you wish to test:

```
In [1]: import app

In [2]: app.sleep.apply_async([1])
Out[2]: <AsyncResult: 3d024e9d-8b20-4103-8103-d6720e623918>
```

On the worker terminal tab, you should see Celery's logging that the task has
run, and Scout's logging around the request being tracked.
