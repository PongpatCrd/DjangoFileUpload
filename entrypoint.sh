#!/bin/bash

set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput

gunicorn --access-logfile - --error-logfile - -b 0.0.0.0:8080 -t 300 --threads 16 send.wsgi:application
