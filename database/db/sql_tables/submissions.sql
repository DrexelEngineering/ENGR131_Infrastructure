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
    CONSTRAINT submissions_pkey PRIMARY KEY (submission_id),
    CONSTRAINT submissions_assignment_id_fkey FOREIGN KEY (assignment_id)
        REFERENCES public.assignments (assignment_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.submissions
    OWNER to admin;

REVOKE ALL ON TABLE public.submissions FROM student;
REVOKE ALL ON TABLE public.submissions FROM teaching_assistant;

GRANT ALL ON TABLE public.submissions TO admin;

GRANT INSERT ON TABLE public.submissions TO student;

GRANT SELECT ON TABLE public.submissions TO teaching_assistant;