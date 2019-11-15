RQ
==

For testing the RQ integration in its simplest context.

Setup
-----

Run redis with:

```
$ docker run --detach --name redis --publish 6379:6379 redis:5.0.4-alpine
```

Set up the local environment:

```
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Run the worker with:

```
$ export SCOUT_KEY=your-key-here
$ rq worker --config app_config --worker-class scout_apm.rq.Worker
```

You should see startup logging from both RQ and Scout.

Start another terminal, activate the virtual environment, and open IPython:

```
$ source venv/bin/activate
$ ipython
```

Then add import and enqueue tasks as you wish to test:

```
In [1]: import app

In [2]: app.queue.enqueue(app.hello)
Out[2]: Job('51c87d5b-e8c7-4e3d-97d8-bff59f2c0a38', enqueued_at=datetime.datetime(2019, 11, 15, 15, 34, 11, 738685))
```

On the worker terminal tab, you should see RQ's logging that the task has run,
and Scout's logging around the request being tracked.
