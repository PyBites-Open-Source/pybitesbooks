#!/usr/bin/env sh

# Simple start up script to use in docker so that we can build the DB and then run the server.
python manage.py migrate

python manage.py runserver 0.0.0.0:8000