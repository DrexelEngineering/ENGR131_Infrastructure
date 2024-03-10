#!/bin/sh

cd /usr/src/apps

echo "Waiting for postgres..."

# this is a hack to wait for postgres to start
while ! nc -z postgres 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

#gunicorn -b 0.0.0.0:5200 app_student:app --timeout 600
gunicorn -w 8 -k gevent -b 0.0.0.0:5200 app_student:app --timeout 600
