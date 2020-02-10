-- Table: public.clients

-- DROP TABLE public.clients;

CREATE TABLE public.clients
(
    "Id" integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    "ClientId" character varying(128) COLLATE pg_catalog."default" NOT NULL,
    "ClientSecret" character varying(256) COLLATE pg_catalog."default" NOT NULL,
    "IsAdmin" boolean NOT NULL,
    CONSTRAINT clients_pkey PRIMARY KEY ("Id")
)

TABLESPACE pg_default;

ALTER TABLE public.clients
    OWNER to postgres;

GRANT SELECT ON TABLE public.clients TO authdb_read;

GRANT ALL ON TABLE public.clients TO postgres;