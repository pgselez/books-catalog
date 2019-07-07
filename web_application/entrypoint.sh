#! /bin/sh

python manage.py migrate
python manage.py runserver web:8000
