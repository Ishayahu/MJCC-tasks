CREATE TABLE todoes_task_file (
    id integer NOT NULL,
    task_id integer NOT NULL,
    file_id integer NOT NULL
);


ALTER TABLE public.todoes_task_file OWNER TO puser;

CREATE SEQUENCE todoes_task_file_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.todoes_task_file_id_seq OWNER TO puser;
ALTER SEQUENCE todoes_task_file_id_seq OWNED BY todoes_task_file.id;
ALTER TABLE ONLY todoes_task_file ALTER COLUMN id SET DEFAULT nextval('todoes_task_file_id_seq'::regclass);
ALTER TABLE ONLY todoes_task_file
    ADD CONSTRAINT todoes_task_file_pkey PRIMARY KEY (id);
ALTER TABLE ONLY todoes_task_file
    ADD CONSTRAINT todoes_task_file_task_id_file_id_key UNIQUE (task_id, file_id);
ALTER TABLE ONLY todoes_task_file
    ADD CONSTRAINT task_id_refs_id_125ace27 FOREIGN KEY (task_id) REFERENCES todoes_task(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY todoes_task_file
    ADD CONSTRAINT todoes_task_file_file_id_fkey FOREIGN KEY (file_id) REFERENCES todoes_file(id) DEFERRABLE INITIALLY DEFERRED;