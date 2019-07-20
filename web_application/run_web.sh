#! /bin/sh

python manage.py makemigrations
python manage.py migrate

rm -r static_root/*

python manage.py collectstatic

gunicorn --workers=4 --reload --bind=web:8000 books_catalog.wsgi:application
