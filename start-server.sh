##!/usr/bin/env bash
## start-server.sh
#if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
#    (cd /opt/CivicsTest; python manage.py createsuperuser --no-input)
#fi
#(cd /opt/CivicsTest; gunicorn CivicsTest.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3) &
#nginx -g "daemon off;"


#!/bin/sh


echo "Initializing postgres db..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "postgres database has initialized successfully"
fi

exec "$@"