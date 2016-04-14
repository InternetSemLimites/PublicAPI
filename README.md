# Internet Sem Limites - CMS 

[CMS](https://internetsemlimites.herokuapp.com) for [InternetSemLimites](https://github.com/InternetSemLimites/InternetSemLimites) colaborative list.

## Entry points

* Create new providers: [`/new`](https://internetsemlimites.herokuapp.com/new/)
* Auto generated `README.md` ([main repository](https://github.com/InternetSemLimites/InternetSemLimites)): [`/README.md`](https://internetsemlimites.herokuapp.com/README.md)
* API (JSON data):
* * [All providers `/`](https://internetsemlimites.herokuapp.com/)
* * [Hall of Fame `/fame/`](https://internetsemlimites.herokuapp.com/fame/)
* * [Hall of Shame `/shame/`](https://internetsemlimites.herokuapp.com/shame/)
* * [By state `/<state abbreviation>/`](https://internetsemlimites.herokuapp.com/sc/)
* * [Hall of Fame by region `/<state abbreviation>/fame/`](https://internetsemlimites.herokuapp.com/sc/fame/) 
* * [Hall of Shame by region `/<state abbreviation>/shame/`](https://internetsemlimites.herokuapp.com/sc/shame/)

## Install

### Requirements

The CMS is based in [Python](http://python.org) 3 and [Django](http://djangoproject.com).

Once you have `pip` available let's install the dependencies:

```
pip install -r requirements.txt
```

### Settings

Copy `contrib/.env.sample` as `.env` in the project's root folder and adjust your settings.

### Migrations

Once you're done with requirements, dependencies and settings, create the basic structure at the database and create a super-user for you:

```
python manage.py migrate
python manage.py createsuperuser
```

### Generate static files

We serve static files through [WhiteNoise](http://whitenoise.evans.io), so depending on your configuration you might have to run:

```
python manage.py collectstatic
```

### Ready?

Not sure? Run `python manage.py check` and `python manage.py test` just in case.

### Ready!

Run the server with `python manage.py runserver` and load [localhost:8000](http://localhost:8000) with your favorite browser.

## License

Licensed under the [MIT License](LICENSE).
