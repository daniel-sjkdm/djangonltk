# djangonltk

This web app was created to understand the basic deployment process on _Heroku_ with django as backend server and postgresql as database.

The libraries I used were:

+ django: backend 
+ django-rest-framework: rest api 
+ django-cors-headers: unblock the CORS headers policy
+ nltk: natural language processing
+ praw: reddit api for python
+ jquery: front end


## Development steps

### Creating environment and installing requirements

```sh
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install requirements.txt
```


## Deployment steps

### Step 1: Create an account

Create a Heroku account at https://www.heroku.com/, you shouldn't register a credit card to start using their services.


### Step 2: Downloading Heroku CLI and loging in

Only for unix like systems:

```
$ curl https://cli-assets.heroku.com/install.sh | sh
```

The full documentation is at https://devcenter.heroku.com/articles/heroku-cli.

Then you can login from the heroku cli with the login command and choose the auth method you like:

```
$ heroku login
```

### Step 3: Creating the app and database

Create the application and the postgresql database as an add on feature:

```
$ heroku create <app_name>
$ heroku addons 
```

### Step 4: Configure the heroku repository

Once the application and its add ons are created it's time to configure the heroku repository:

```
$ heroku
```


### Step 4: Installing dependencies and configure the settings

Install the following libraries:

+ whitenoise: automatically serve the static content in heroku 
+ dj-database-url: connect to postgresql inside heroku with a DATABASE_URL that's created automatically
+ django_heroku: configure the django app to work inside heroku

```
$ pip install whitenoise dj-database-url django_heroku
```

In the project's settings.py file add the following content:

```
import django_heroku
import dj_database_url

...

ALLOWED_HOSTS = [
    ...,
    "https://<heroku_app_name>.herokuapp.com"
]

...

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    ...
]

...

DATABASES = {
    ...
}

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

...

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# This goes at the bottom 

django_heroku.settings(locals())

```


### Step 5: Push everything inside

It's time to push the repository to Heroku:

```
$ git push heroku master
```

Then, run the database migrations commands:

```
$ heroku run python manage.py makemigrations
$ heroku run python manage.py migrate
```

Finally, everything is configured as it should be. So go to the Heroku app's url and enjoy.
