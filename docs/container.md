---
layout: default
---

# Docker compose container layout.

The docker-compose file defines 3 services redis, web and celery. Both web and celery are based on the Dockerfile but lets go through them really fast

---
## Dockerfile

```
FROM python:3.6

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN useradd -ms /bin/bash webapp

COPY . .
```

---
```
FROM python:3.6
```
We are basing the image on python 3.6

```
WORKDIR /user/src/app
```
The working directory will be `/usr/src/app`, this is where the application's code will reside.

```
COPY requirements.txt .
```
Copy the requirements.txt to `/usr/src/app`
```
RUN pip install --no-cache-dir -r requirements.txt
```
Install the python requirements from `requirements.txt`
```
RUN useradd -ms /bin/bash webapp
```
Add our `webapp` user that the application will run from
```
COPY . .
```
Copy the application's code into the container.

---

This is a fairly straightforward dockerfile, nothing really complicated here. It's basically installing our application into an image that can be run

## Docker-compose.yml

The docker compose file get's a bit more interesting.
```
version: '2'
services:
  x-web: &web-base
    build: .
    environment:
      - APP_NAME=app
      - APPLICATION=japp
      - UWSGI_APP_LOGGING_ENABLED=true
      - FLASK_ENV=development
    volumes:
      - .:/usr/src/app

  redis:
    restart: unless-stopped
    image: redis:5-alpine
    volumes:
      - ./data/redis:/data

  web:
    <<: *web-base
    restart: unless-stopped
    links:
      - redis
      - celery
    ports:
      - '8000:8000'
    command: uwsgi --ini /usr/src/app/uwsgi.ini
  
  celery:
    <<: *web-base
    links:
      - redis
    command: ["celery", "worker", "-l", "debug", "-A", "app.tasks", "--uid", "webapp"]
```

In the compose file we are defining 4 services, 3 of which will be running.

- x-web
    - This is a "base" for our `web` and `celery` services
- redis
    - This is the redis server
- web
    - This is our web application
- celery
    - This is the celery service

---

x-web is built from the [Dockerfile](#dockerfile), sets up some environment variables that we need to run the application and attaches the current directory to the container with the `volumes` section.

web uses everything from `x-web` as it's base, links the `redis` and `celery` services to the service, opens port `8000` and runs [uWsgi](#uwsgi) as the server.

celery uses everything from `x-web`, links to the `redis` service and runs celery.

web command explanation

- `uwsgi --ini /usr/src/app/uwsgi.ini` Runs [uWsgi](#uwsgi) with the configuration file in `/usr/src/app/uwsgi.ini`, which is in the checkout as `uwsgi.ini` and explained below.

celery command explanation

- `command: ["celery", "worker", "-l", "debug", "-A", "app.tasks", "--uid", "webapp"]` Runs the celery worker with the logging level of `debug` using the application defined in `app.tasks` as the user `webapp`. 

---

## uWsgi

[uWsgi](https://uwsgi-docs.readthedocs.io/en/latest/) is a very complete application server with built in support for http. Lets look at the uwsgi.ini file

```ini
[uwsgi]

chdir = /usr/src/app
; home = /apps/venv-snap
module = app.wsgi

master = true
uid = webapp
gid =  webapp

logger-list = true
http=:8000
; threaded-logger = true

# We need to turn off the file-wrapper on newer versions of uwsgi
# the wrapper kills flasks send_file function.
wsgi-disable-file-wrapper = true
touch-reload=/usr/src/app/uwsgi.ini
die-on-term = true

py-autoreload = 1
worker-reload-mercy=5
```

There's a lot going on in this file lets go through it in chunks so it's a bit more manageable

```ini
[uwsgi]
```
This defines the `uwsgi` section. By default uwsgi uses the `uwsgi` section but you can name it anything you want. We are keeping it as `uwsgi` here as a standard practice.

```ini
chdir = /usr/src/app
; home = /apps/venv-snap
module = app.wsgi
```
Here we are telling uwsgi to change to `/user/src/app` as the working directory and to use the file `app/wsgi.py` to create a wsgi app. By default uwsgi is going to look for a variable called `application` inside of `app/wsgi.py` that is a [callable](https://stackoverflow.com/a/111255) wsgi application. The details here are not important.

```ini
master = true
uid = webapp
gid =  webapp
```

Here we are setting uWsgi up to have a master process and to change to the `webapp` user and group. The master process is generally used for graceful reloading of the application and probably is not used that much in this application but it's nice to have so leaving it here doesn't cause issues. 

```ini
logger-list = true
http=:8000
; threaded-logger = true
```

Here we are telling uwsgi to list the available loggers for good measure and starting the built in http server listening on port `8000` of all interfaces.

```ini
# We need to turn off the file-wrapper on newer versions of uwsgi
# the wrapper kills flasks send_file function.
wsgi-disable-file-wrapper = true
touch-reload=/usr/src/app/uwsgi.ini
die-on-term = true
```

Here we are disabling the built in file wrapper for uwsgi because it does not play nice with flask's send-file, this will be useful when we start sending image responses from the application. `touch-reload` makes it so that we can reload the uwsgi server when the ini file is modified. `die-on-term` makes uwsgi play nice with docker, uwsgi will be process #1 so when docker tries to shut the container down a `TERM` signal will be sent which uwsig normally does not shut down from. `die-on-term` makes uwsgi die when it gets a `TERM` signal.

```ini
py-autoreload = 1
worker-reload-mercy=5
```

This part autoreloads uwsgi wheen any python files change and makes it so that workers are killed in 5 seconds or less with `worker-reload-mercy`.
