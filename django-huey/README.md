Django-Huey
===========

For testing the [Huey](https://huey.readthedocs.io/en/latest/)
integration running [with
Django](https://huey.readthedocs.io/en/latest/django.html).

Setup
-----

**First,** set up your local environment:

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

**Second,** run the Huey worker with:

```
$ export SCOUT_KEY=your-key-here
$ python app.py run_huey
```

You should see startup logging from both Huey and Scout.

**Third,** start another terminal, activate the virtual environment, and open
IPython via Django:

```
$ source venv/bin/activate
$ python app.py shell
```

Here you can import and enqueue tasks as you wish to test:

```
In [1]: import tasks

In [2]: tasks.hello()
Out[2]: <Result: task b645e1c2-1df4-487d-b232-ce23dadb2255>
```

On the worker terminal tab, you should see Huey's logging that the task has
run, and Scout's logging around the request being tracked.
