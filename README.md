# Internet Sem Limites - CMS 

[CMS (Content Management System)](https://internetsemlimites.herokuapp.com) for [InternetSemLimites](https://github.com/InternetSemLimites/InternetSemLimites) colaborative list.

## Entry points

### API

* [All providers `GET /api/`](https://internetsemlimites.herokuapp.com/api/)
* [Hall of Fame `GET /api/fame/`](https://internetsemlimites.herokuapp.com/api/fame/)
* [Hall of Shame `GET /api/shame/`](https://internetsemlimites.herokuapp.com/api/shame/)
* [By state `GET /api/<state abbreviation>/`](https://internetsemlimites.herokuapp.com/api/sc/)
* [Hall of Fame by region `GET /api/<state abbreviation>/fame/`](https://internetsemlimites.herokuapp.com/api/sc/fame/) 
* [Hall of Shame by region `GET /api/<state abbreviation>/shame/`](https://internetsemlimites.herokuapp.com/api/sc/shame/)

#### API Headers

All API requests returns a JSON with list(s) of providers (`providers`, `hall-of-fame` or `hall-of-shame`). Each provider is an obejct with the following properties:

* `category`: _Hall of Fame_ or for _Hall of Shame_
* `coverage`: List os states covered by this provider
* `created_at`: Dated the provider was submitted to our server
* `name`: Name of the provider
* `other`: General information (e.g.: cities covered, residential and/or corporative only etc.)
* `source`: URL for the source of the info (usually an  [archive.is](http://archive.is) link)
* `url`: URL of the provider


### CMS

* Create new providers: [`GET/POST /new`](https://internetsemlimites.herokuapp.com/new/)

### Auto generated markdown files ([main repository](https://github.com/InternetSemLimites/InternetSemLimites))

* `README.md` : [`GET /markdown/README.md`](https://internetsemlimites.herokuapp.com//markdown/README.md)
* `HALL_OF_SHAME.md`: [`GET /markdown/HALL_OF_SHAME.md`](https://internetsemlimites.herokuapp.com/markdown/HALL_OF_SHAME.md)

## Install

### Requirements

The CMS is based in [Python](http://python.org) 3 and [Django](http://djangoproject.com). Once you have `pip` available, install the dependencies:

```console
python -m pip install -r requirements.txt
```

### Settings

Copy `contrib/.env.sample` as `.env` in the project's root folder and adjust your settings.

### Migrations

Once you're done with requirements, dependencies and settings, create the basic structure at the database and create a super-user for you:

```console
python manage.py migrate
python manage.py createsuperuser
```

### Generate static files

We serve static files through [WhiteNoise](http://whitenoise.evans.io), so depending on your configuration you might have to run:

```console
python manage.py collectstatic
```

### Ready?

Not sure? Run `python manage.py check` and `python manage.py test` just in case.

### Ready!

Run the server with `python manage.py runserver` and load [localhost:8000](http://localhost:8000) in your favorite browser.

## License

Licensed under the [MIT License](LICENSE).