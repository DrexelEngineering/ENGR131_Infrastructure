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