#!/bin/bash

set -e

python manage.py migrate --noinput
python manage.py crontab remove
python manage.py crontab add
python manage.py crontab show

gunicorn --access-logfile - --error-logfile - -b 0.0.0.0:8080 -t 300 --threads 16 send.wsgi:application

# gunicorn send.wsgi:application --timeout 300 --threads 16 -b :8080