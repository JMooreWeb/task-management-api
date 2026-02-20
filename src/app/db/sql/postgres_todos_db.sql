-- Table: public.Users
-- DROP TABLE IF EXISTS public.Users;
CREATE TABLE IF NOT EXISTS public.Users
(
    id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass),
    email character varying(200) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    username character varying(45) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    first_name character varying(45) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    last_name character varying(45) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    hashed_password character varying(200) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    role character varying(45) COLLATE pg_catalog."default",
    is_active boolean,
    CONSTRAINT users_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.Users
    OWNER to postgres;


-- Table: public.Todos
-- DROP TABLE IF EXISTS public.Todos;
CREATE TABLE IF NOT EXISTS public.Todos
(
    id integer NOT NULL DEFAULT nextval('todos_id_seq'::regclass),
    user_id integer,
    CONSTRAINT todos_pkey PRIMARY KEY (id),
    CONSTRAINT fk_user FOREIGN KEY (user_id)
        REFERENCES public.Users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION    
    title character varying(200) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    description character varying(500) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    due_date date DEFAULT NULL,
    is_completed boolean DEFAULT false,
    created_at timestamp with time zone DEFAULT now(),
    completed_at timestamp with time zone DEFAULT NULL
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.Todos
    OWNER to postgres;
