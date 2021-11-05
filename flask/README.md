Django
======

For testing the [Flask](https://flask.palletsprojects.com/) integration.

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
$ flask run
```

You should see startup logging from Flask and Scout.

**Third,** visit pages in your browser, such as http://localhost:5000/ .
