# interpret: bash
#!/bin/sh
set -e

echo "Running migrations..."
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate

echo "Collecting static files..."
pipenv run python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec pipenv run gunicorn shopping.wsgi:application --bind 0.0.0.0:8000
#--workers 3 --timeout 120 --log-level info