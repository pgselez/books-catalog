#! /bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic

gunicorn --workers=4 --bind=web:8000 books_catalog.wsgi:application
