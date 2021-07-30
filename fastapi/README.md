FastAPI
=======

For testing the [FastAPI](https://fastapi.tiangolo.com/) integration.

Setup
-----

**First,** set up your local environment (Python 3.6+):

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

**Second,** run the app with:

```
$ export SCOUT_KEY=your-key-here
$ python -X dev app.py  # -X dev only supported on Python 3.7+
```

You should see startup logging from Scout and FastAPI.

**Third,** visit pages in your browser, such as http://localhost:8000/ .
