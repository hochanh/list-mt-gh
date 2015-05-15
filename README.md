Deployment to Heroku
====================

## Get things:

```bash
wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh
sudo apt-get install postgresql
```

If you catch this error:

```
psql: could not connect to server: No such file or directory
    Is the server running locally and accepting
    connections on Unix domain socket "/var/run/postgresql/.s.PGSQL.5432"?
```

then try reinstall it all from scratch

```
sudo apt-get remove --purge postgresql\*
sudo apt-get install postgresql
```

## Config things:

### 1. PostGreSQL

Login to user `postgres`

```bash
sudo su postgres
psql
```
and manipulate database:

```sql
CREATE USER testadmin WITH CREATEDB PASSWORD 'testing';
CREATE DATABASE django_testdb OWNER testadmin;
```
If you want to drop all tables in your database:

```sql
psql -d django_testdb
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
```

Remember to make migrations again:

```bash
python3 manage.py makemigrations
```

### 2. Set up local Django App

After having a Django app run smoothly on SQLite3:

Get some packages for production:

```bash
# use heroku app lists
pip3 install django-toolbelt

# or do it yourself
pip3 install -r requirements.txt
```

and for testing (another virtual environment):

```bash
pip3 install -r requirements_tests.txt
```

Add this to `settings.py` to parse database config from varialbe $DATABASE_URL

```bash
# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

Now set $DATABASE_URL in fish as such:

```bash
set -x DATABASE_URL "postgres://testadmin:testing@localhost/django_testdb"
```

Don't forget to migrate new data:

```bash
python3 manage.py migrate --noinput
python3 manage.py makemigrations
```

### 3. Set up Heroku

Set `Procfile` to:

```
web: waitress-serve --port=$PORT superlists.wsgi:application
```

and `runtime.txt` to:

```
python-3.4.2
```

All done now, push it to Heroku and twist a beer!

then `syncdb` (I don't know what it is, if nothing works, then you should try it)

```
python3 manage.py syncdb
```

Set VARS:

```bash
heroku config:add DJANGO_SETTINGS_MODULE=superlists.settings
heroku config:add SECRET_KEY='kua-17^*_m%7y'
```

for Stagging site:

```bash
heroku config:add DJANGO_SETTINGS_MODULE=superlists.settings
```

Put those VARS to fish environment to developing offline:

```bash
function superlists --on-event virtualenv_did_activate:tdd_test
    set -gx DJANGO_SETTINGS_MODULE superlists.settings_tests
    set -gx SECRET_KEY 'kua-17^*_m%7y'
end
```

### 4. Start and Stop app

Start the app manually:

```bash
heroku ps:scale web=1
```

and stop it:

```bash
heroku ps:scale web=0
```

### 5. Setup static files

Put this to `settings.py`

```python
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
```

Put this to `base.html`

```html
{% load static from staticfiles %}
```

Put this to `wsgi.py`

```python
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise


application = get_wsgi_application()
application = DjangoWhiteNoise(application)
```


