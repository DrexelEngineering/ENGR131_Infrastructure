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