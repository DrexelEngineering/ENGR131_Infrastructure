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