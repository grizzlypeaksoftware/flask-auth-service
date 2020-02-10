-- Table: public.blacklist

-- DROP TABLE public.blacklist;

CREATE TABLE public.blacklist
(
    token character varying(256) COLLATE pg_catalog."default" NOT NULL
)

TABLESPACE pg_default;

ALTER TABLE public.blacklist
    OWNER to postgres;