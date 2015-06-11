CREATE TABLE todoes_regulartask_file (
    id integer NOT NULL,
    regulartask_id integer NOT NULL,
    file_id integer NOT NULL
);


ALTER TABLE public.todoes_regulartask_file OWNER TO puser;

CREATE SEQUENCE todoes_regulartask_file_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.todoes_regulartask_file_id_seq OWNER TO puser;
ALTER SEQUENCE todoes_regulartask_file_id_seq OWNED BY todoes_regulartask_file.id;
ALTER TABLE ONLY todoes_regulartask_file ALTER COLUMN id SET DEFAULT nextval('todoes_regulartask_file_id_seq'::regclass);
ALTER TABLE ONLY todoes_regulartask_file
    ADD CONSTRAINT todoes_regulartask_file_pkey PRIMARY KEY (id);
ALTER TABLE ONLY todoes_regulartask_file
    ADD CONSTRAINT todoes_regulartask_file_regulartask_id_file_id_key UNIQUE (regulartask_id, file_id);
ALTER TABLE ONLY todoes_regulartask_file
    ADD CONSTRAINT regulartask_id_refs_id_125ace27 FOREIGN KEY (regulartask_id) REFERENCES todoes_regulartask(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY todoes_regulartask_file
    ADD CONSTRAINT todoes_regulartask_file_file_id_fkey FOREIGN KEY (file_id) REFERENCES todoes_file(id) DEFERRABLE INITIALLY DEFERRED;