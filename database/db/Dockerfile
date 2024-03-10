# base image
FROM postgres:13-alpine

# Set permissions and run the script to create create_db.sql
# this is a special directory that will execute any SQL scripts inside it
# it will also store the files there.
ADD create_db.sql /docker-entrypoint-initdb.d/

