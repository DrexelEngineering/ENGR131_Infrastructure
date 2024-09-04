CREATE DATABASE grades;

-- create the student user with only write access
CREATE ROLE student WITH LOGIN PASSWORD '${STUDENT_PASSWORD}';

-- create the teaching assistant role with only read access
CREATE ROLE teaching_assistant WITH LOGIN PASSWORD '${TEACHING_ASSISTANT_PASSWORD}';

-- creates the faculty role with read and write access
CREATE ROLE faculty WITH LOGIN PASSWORD '${FACULTY_PASSWORD}';

-- create an admin account
CREATE ROLE admin WITH LOGIN PASSWORD '${ADMIN_PASSWORD}';

-- Grants superuser access to the admin account
ALTER ROLE admin WITH SUPERUSER;

\c grades

GRANT INSERT on ALL TABLES IN SCHEMA public TO student;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT INSERT ON TABLES TO student;

GRANT SELECT on ALL TABLES IN SCHEMA public TO teaching_assistant;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO teaching_assistant;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO faculty;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO faculty;

-- Table: public.assignments

-- DROP TABLE IF EXISTS public.assignments;

CREATE TABLE IF NOT EXISTS public.assignments
(
    assignment_name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    assignment_id character varying(50) COLLATE pg_catalog."default" NOT NULL,
    assignment_type character varying(50) COLLATE pg_catalog."default",
    assignment_num integer,
    CONSTRAINT assignments_pkey PRIMARY KEY (assignment_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.assignments
    OWNER to admin;

REVOKE ALL ON TABLE public.assignments FROM student;
REVOKE ALL ON TABLE public.assignments FROM teaching_assistant;

GRANT ALL ON TABLE public.assignments TO admin;

GRANT INSERT ON TABLE public.assignments TO student;

GRANT SELECT ON TABLE public.assignments TO teaching_assistant;

-- Table: public.lab_section

-- DROP TABLE IF EXISTS public.lab_section;

CREATE TABLE IF NOT EXISTS public.lab_section
(
    coursecode character varying(255) COLLATE pg_catalog."default",
    sessiontype character varying(255) COLLATE pg_catalog."default",
    deliverymode character varying(255) COLLATE pg_catalog."default",
    sessionnumber character varying(255) COLLATE pg_catalog."default",
    courseid integer,
    coursetitle character varying(255) COLLATE pg_catalog."default",
    dayofweek character varying(10) COLLATE pg_catalog."default",
    timeslot character varying(255) COLLATE pg_catalog."default",
    instructors character varying(255) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.lab_section
    OWNER to admin;

REVOKE ALL ON TABLE public.lab_section FROM student;
REVOKE ALL ON TABLE public.lab_section FROM teaching_assistant;

GRANT ALL ON TABLE public.lab_section TO admin;

GRANT INSERT ON TABLE public.lab_section TO student;

GRANT SELECT ON TABLE public.lab_section TO teaching_assistant;

-- Table: public.live_submissions

-- DROP TABLE IF EXISTS public.live_submissions;

CREATE TABLE IF NOT EXISTS public.live_submissions
(
    submission_id character varying(500) COLLATE pg_catalog."default",
    student_id character varying(50) COLLATE pg_catalog."default" NOT NULL,
    assignment_id character varying(50) COLLATE pg_catalog."default",
    submitter_type character varying(50) COLLATE pg_catalog."default",
    score double precision,
    max_score double precision,
    submission_time timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    student_response text COLLATE pg_catalog."default",
    question_id character varying(50) COLLATE pg_catalog."default",
    ip_address character varying(50) COLLATE pg_catalog."default",
    hostname character varying(50) COLLATE pg_catalog."default",
    jupyter_user character varying(50) COLLATE pg_catalog."default",
    response_time time with time zone
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.live_submissions
    OWNER to admin;

REVOKE ALL ON TABLE public.live_submissions FROM faculty;
REVOKE ALL ON TABLE public.live_submissions FROM student;
REVOKE ALL ON TABLE public.live_submissions FROM teaching_assistant;

GRANT ALL ON TABLE public.live_submissions TO admin;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE public.live_submissions TO faculty;

GRANT INSERT ON TABLE public.live_submissions TO student;

GRANT SELECT ON TABLE public.live_submissions TO teaching_assistant;

COMMENT ON COLUMN public.live_submissions.response_time
    IS 'response time from local timestamp';

-- Table: public.questions

-- DROP TABLE IF EXISTS public.questions;

CREATE TABLE IF NOT EXISTS public.questions
(
    question_id integer NOT NULL,
    assignment_id character varying(50) COLLATE pg_catalog."default" NOT NULL,
    question_name text COLLATE pg_catalog."default",
    max_score double precision,
    visible boolean,
    CONSTRAINT questions_pkey PRIMARY KEY (assignment_id, question_id),
    CONSTRAINT questions_assignment_id_fkey FOREIGN KEY (assignment_id)
        REFERENCES public.assignments (assignment_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.questions
    OWNER to admin;

REVOKE ALL ON TABLE public.questions FROM student;
REVOKE ALL ON TABLE public.questions FROM teaching_assistant;

GRANT ALL ON TABLE public.questions TO admin;

GRANT INSERT ON TABLE public.questions TO student;

GRANT SELECT ON TABLE public.questions TO teaching_assistant;

-- Table: public.students_enrolled

-- DROP TABLE IF EXISTS public.students_enrolled;

CREATE TABLE IF NOT EXISTS public.students_enrolled
(
    student_id character varying(50) COLLATE pg_catalog."default" NOT NULL,
    first_name character varying(20) COLLATE pg_catalog."default",
    last_name character varying(20) COLLATE pg_catalog."default",
    course character varying(8) COLLATE pg_catalog."default",
    year integer,
    section character varying(50) COLLATE pg_catalog."default",
    lab_section character varying(100) COLLATE pg_catalog."default",
    semester character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT students_enrolled_pkey PRIMARY KEY (student_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.students_enrolled
    OWNER to admin;

REVOKE ALL ON TABLE public.students_enrolled FROM student;
REVOKE ALL ON TABLE public.students_enrolled FROM teaching_assistant;

GRANT ALL ON TABLE public.students_enrolled TO admin;

GRANT INSERT ON TABLE public.students_enrolled TO student;

GRANT SELECT ON TABLE public.students_enrolled TO teaching_assistant;

-- Table: public.students_lab_section

-- DROP TABLE IF EXISTS public.students_lab_section;

CREATE TABLE IF NOT EXISTS public.students_lab_section
(
    lastname character varying(255) COLLATE pg_catalog."default",
    firstname character varying(255) COLLATE pg_catalog."default",
    middlename character varying(255) COLLATE pg_catalog."default",
    levelname character varying(255) COLLATE pg_catalog."default",
    classificationname character varying(255) COLLATE pg_catalog."default",
    majorname character varying(255) COLLATE pg_catalog."default",
    emailaddress character varying(255) COLLATE pg_catalog."default",
    student_id character varying(255) COLLATE pg_catalog."default" NOT NULL,
    zoomid character varying(255) COLLATE pg_catalog."default",
    sectionnumber integer,
    starttime time with time zone,
    endtime time with time zone,
    day_of_week text COLLATE pg_catalog."default",
    CONSTRAINT pk_student_id PRIMARY KEY (student_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.students_lab_section
    OWNER to admin;

REVOKE ALL ON TABLE public.students_lab_section FROM student;
REVOKE ALL ON TABLE public.students_lab_section FROM teaching_assistant;

GRANT ALL ON TABLE public.students_lab_section TO admin;

GRANT INSERT ON TABLE public.students_lab_section TO student;

GRANT SELECT ON TABLE public.students_lab_section TO teaching_assistant;

-- Table: public.submissions

-- DROP TABLE IF EXISTS public.submissions;

CREATE TABLE IF NOT EXISTS public.submissions
(
    submission_id character varying(50) COLLATE pg_catalog."default" NOT NULL,
    original_file_name character varying(255) COLLATE pg_catalog."default",
    student_id character varying(50) COLLATE pg_catalog."default" NOT NULL,
    assignment_id character varying(50) COLLATE pg_catalog."default" NOT NULL,
    submitter_type character varying(50) COLLATE pg_catalog."default" NOT NULL,
    total_score double precision,
    max_score double precision,
    percentage_score double precision,
    submission_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    start_time timestamp without time zone,
    end_time timestamp without time zone,
    flag character varying(255) COLLATE pg_catalog."default",
    submission_mechanism text COLLATE pg_catalog."default",
    logfile text COLLATE pg_catalog."default",
    CONSTRAINT submissions_pkey PRIMARY KEY (submission_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.submissions
    OWNER to admin;

REVOKE ALL ON TABLE public.submissions FROM faculty;
REVOKE ALL ON TABLE public.submissions FROM student;
REVOKE ALL ON TABLE public.submissions FROM teaching_assistant;

GRANT ALL ON TABLE public.submissions TO admin;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE public.submissions TO faculty;

GRANT INSERT ON TABLE public.submissions TO student;

GRANT SELECT ON TABLE public.submissions TO teaching_assistant;