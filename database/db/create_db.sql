CREATE DATABASE grades;

-- create the student user with only write access
CREATE ROLE student WITH LOGIN PASSWORD 'coauthor-lucrative-sensitive';

-- create the teaching assistant role with only read access
CREATE ROLE teaching_assistant WITH LOGIN PASSWORD 'seducing-mountain-numeral';

-- creates the faculty role with read and write access
CREATE ROLE faculty WITH LOGIN PASSWORD 'monument-apache-tricky';

-- create an admin account
CREATE ROLE admin WITH LOGIN PASSWORD 'curve-strained-enlisted';

-- Grants superuser access to the admin account
ALTER ROLE admin WITH SUPERUSER;

\c grades

GRANT INSERT on ALL TABLES IN SCHEMA public TO student;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT INSERT ON TABLES TO student;

GRANT SELECT on ALL TABLES IN SCHEMA grades TO teaching_assistant;
ALTER DEFAULT PRIVILEGES IN SCHEMA grades GRANT SELECT ON TABLES TO teaching_assistant;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO faculty;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO faculty;


