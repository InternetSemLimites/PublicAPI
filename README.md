# Internet Sem Limites - CMS 

[CMS](https://internetsemlimites.herokuapp.com) para a lista colaborativa [InternetSemLimites](https://github.com/jlcarvalho/InternetSemLimites).

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
