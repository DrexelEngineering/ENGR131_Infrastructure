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