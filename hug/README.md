Hug
===

For testing the [Hug](https://www.hug.rest/) integration.

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

**Second,** run the app with:

```
$ export SCOUT_KEY=your-key-here
$ hug -f app.py
```

You should see startup logging from Hug and Scout.

**Third,** visit pages in your browser, such as http://localhost:8080/ .
