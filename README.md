# Jaryan
"Jaryan" in Persian means stream, story, trend or even thread! Jaryan is a reddit-like social community aims more control and be more scalable and flexible.

Notice: you'll see in codes that "Jaryanak" used to call models. You can imagine that like sub-Jaryan or small Jaryan. 

## Requirements
Jaryan is based on Django (a python web framework). You can install requirements using following command:
```
pip install -r requirements.text

```
You need to download & install redis too, on MacOS X you may use brew package manager to do it:
```
brew install redis
```
Check [here](http://redis.io/download) for official redis documentation.

## Running
Before running the webserver you have to start redis and Django-Celery :
```
redis-server
celery -A NAME worker -B --loglevel=info
```
Replace NAME with "altio" or whatever you've set.

Finally create the tables in the database and run the server:
```
python manage.py makemigration
python manage.py migrate
python manage.py runserver
```
Also you may want to create a superuser before running server:
```
python manage.py createsuperuser
```

## TODO
- [ ] Localization
- [ ] Front-end
- [ ] Writing Tests
