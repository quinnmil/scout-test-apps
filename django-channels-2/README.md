Django-Channels-2
=================

For testing the Django [Channels](https://channels.readthedocs.io/en/latest/)
integration, for Channels version 2.

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
$ python app.py runserver
```

You should see startup logging from Daphne (Channels' async dev server),
Django, and Scout.

**Third,** visit pages in your browser:

* http://localhost:8000/ for a normal Django sync view.
* http://localhost:8000/async/ for a Channels based async view.
