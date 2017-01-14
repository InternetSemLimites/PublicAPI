# Internet Sem Limites: CMS & API

[![Build Status](https://travis-ci.org/InternetSemLimites/PublicAPI.svg?branch=master)](https://travis-ci.org/InternetSemLimites/PublicAPI)
[![Updates](https://pyup.io/repos/github/internetsemlimites/publicapi/shield.svg)](https://pyup.io/repos/github/internetsemlimites/publicapi/)
[![Coverage Status](https://coveralls.io/repos/github/InternetSemLimites/PublicAPI/badge.svg?branch=master)](https://coveralls.io/github/InternetSemLimites/PublicAPI?branch=master)
[![Code Climate](https://codeclimate.com/github/InternetSemLimites/PublicAPI/badges/gpa.svg)](https://codeclimate.com/github/InternetSemLimites/PublicAPI)

[CMS and API](https://internetsemlimites.herokuapp.com) for [InternetSemLimites](http://internetsemlimites.github.io/) colaborative project.

## Entry points

### API

#### List existing providers

* [All providers `GET /api/`](https://internetsemlimites.herokuapp.com/api/)
* [Hall of Fame `GET /api/fame/`](https://internetsemlimites.herokuapp.com/api/fame/)
* [Hall of Shame `GET /api/shame/`](https://internetsemlimites.herokuapp.com/api/shame/)
* [By state `GET /api/<state abbreviation>/`](https://internetsemlimites.herokuapp.com/api/sc/)
* [Hall of Fame by state `GET /api/<state abbreviation>/fame/`](https://internetsemlimites.herokuapp.com/api/sc/fame/) 
* [Hall of Shame by state `GET /api/<state abbreviation>/shame/`](https://internetsemlimites.herokuapp.com/api/sc/shame/)

#### Create new provider
* [Create new provider `POST /api/provider/new/`](https://internetsemlimites.herokuapp.com/api/provider/42/)
* [Provider detail `GET /api/provider/<provider id>/`](https://internetsemlimites.herokuapp.com/api/provider/42/)

#### Edit existing provider
* [Edit existing provider `POST /api/provider/<provider id>/edit/`](https://internetsemlimites.herokuapp.com/api/provider/42/edit/)

#### API Headers

All API requests returns a JSON with list(s) of providers (`providers`, `hall-of-fame` or `hall-of-shame`). Each provider is an obejct with the following properties:

* `category`: _Hall of Fame_ or for _Hall of Shame_
* `coverage`: List os states covered by this provider
* `created_at`: Dated the provider was submitted to our server
* `name`: Name of the provider
* `other`: General information (e.g.: cities covered, residential and/or corporative only etc.)
* `source`: URL for the source of the info (usually an  [archive.is](http://archive.is) link)
* `url`: URL of the provider
* `status`: (only for _provider detail_ endpoint) moderation status
* `moderation_reason`: (only for _provider detail_ endpoint) moderation justification for the status above

### CMS

Anyone can suggest new providers using [our form](https://internetsemlimites.herokuapp.com/new/).

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

Copy `contrib/.env.sample` as `.env` in the project's root folder and adjust your settings. These are the main environment settings:

#### Django settings

* `DEBUG` (_boolean_) enable or disable [Django debug mode](https://docs.djangoproject.com/en/1.9/ref/settings/#debug)
* `SECRET_KEY` (_string_) [Django's secret key](https://docs.djangoproject.com/en/1.9/ref/settings/#std:setting-SECRET_KEY)
* `ALLOWED_HOSTS` (_string_) [Django's allowed hosts](https://docs.djangoproject.com/en/1.9/ref/settings/#allowed-hosts)

#### Database

* `DATABASE_URL` (_string_) [Database URL](https://github.com/kennethreitz/dj-database-url#url-schema)

#### Email settings

* `DEFAULT_FROM_EMAIL` (_string_) default e-maill address to be used as the sender (e.g. `noreply@internetsemlimites.herokuapp.com`)
* `EMAIL_BACKEND` (_string_) Django e-mail backend (e.g. `django.core.mail.backends.console.EmailBackend`)
* SMTP e-mail settings: `EMAIL_HOST` (_string_), `EMAIL_PORT` (_integer_), `EMAIL_USE_TLS` (_boolean_), `EMAIL_HOST_USER` (_string_), and `EMAIL_HOST_PASSWORD` (_string_)

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

If you created a _super-user_ account, you can also use [Django Admin](https://docs.djangoproject.com/en/stable/ref/contrib/admin/) at [`/admin/`](http://localhost:8000/admin/).

## License

Licensed under the [MIT License](LICENSE).
