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