#!/bin/sh

cd /usr/src/apps || exit 1

echo "Waiting for postgres..."

# this is a hack to wait for postgres to start
while ! nc -z postgres 5432; do
	sleep 0.1
done

echo "PostgreSQL started"

# need to extend the timeout for the admin server because there are some batch processes
gunicorn -b 0.0.0.0:5100 app_admin:app --timeout 600
