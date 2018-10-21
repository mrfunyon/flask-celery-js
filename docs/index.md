---
layout: default
---

# Flask Celery and Javascript

## Motivation

Often times front end applications are at the mercy of slow services and a way is needed to make those responses faster. A fake it until you make it type approach sometimes works. This project is a look from a primarially back-end developers perspective to make the front-end of a website more responsive. I am in no way an expert on javascript and am going to stumble my way through making a bridge application.

The final product will be available in the master branch of this repository.

### Whats going to be used?

- Python
    - Flask
    - Celery
- Docker
    - Docker-compose for services
- Redis
    - Broker, message queue and result backend for Docker.
- Jquery
     - All the front-end stuff, as little as I possibly can using promises as much as possible

### Getting to it

App layout

---
![File List](./file_list.png)

Lets take a minute and break down these files
- app
    - Contains the code for the application
    - templates
        - Templates for the app
        - pages
            - index.html
                - the index (for / on our app)
        - base.html
            - base template 
- data
    - data directory for the container.
- docs
    - the static documents (what you are reading right now is index.md).
- logs
    - log directory for the container, mostly just celery logs
- static
    - Static files
    - css
        - css files
    - js
        - js files
        - app.js
            - our js application.
- docker-compose.yml
    - The docker compose file, this contains the services that will be running
- Dockerfile
    - This contains the base image that will be run.
- LICENSE
    - The liscence
- Pipfile
    - Pipfile for local testing, not really useful to us right now
- Pipfile.lock
    - Lock file for our Pipfile to lock down the dependencies
- README.md
    - The readme
- requirements.txt
    - Requirements for running the application
- uwsgi.ini
    - the configuration for uwsgi that our container uses.

--

Building the application.

-----

What is required to run this
- Docker
    - I used docker for mac available from www.docker.com

---

For all of these examples I am going to assume that you are using a terminal either on a mac or a linux machine. I do not have access to a windows machine and did all this on a mac.

---

First checkout the repository
```bash
git clone git@https://github.com/mrfunyon/flask-celery-js.git
```

Then we need to build and start our docker instance.

```bash
docker-compose up --buile
```

Now the example application is available at http://localhost:8000

There's not any real setup you need to do, everything is contained inside of docker. For details on how everything runs see [building the container](container.html)
