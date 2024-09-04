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
    jupyter_user character varying(50) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.live_submissions
    OWNER to admin;

REVOKE ALL ON TABLE public.live_submissions FROM student;
REVOKE ALL ON TABLE public.live_submissions FROM teaching_assistant;

GRANT ALL ON TABLE public.live_submissions TO admin;

GRANT INSERT ON TABLE public.live_submissions TO student;

GRANT SELECT ON TABLE public.live_submissions TO teaching_assistant;