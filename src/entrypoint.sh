#!/usr/bin/env bash

sleep 3

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
#python manage.py create_default_user

python manage.py runserver 0.0.0.0:8000

exec "$@"