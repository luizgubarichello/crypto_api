#!/bin/sh

sleep 10
python manage.py makemigrations

sleep 10
python manage.py migrate

python manage.py runserver 0.0.0.0:8000