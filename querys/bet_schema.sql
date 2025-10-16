--
-- PostgreSQL database dump
--

-- Dumped from database version 15.5 (Ubuntu 15.5-0ubuntu0.23.04.1)
-- Dumped by pg_dump version 15.5 (Ubuntu 15.5-0ubuntu0.23.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: atualiza_saldo(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.atualiza_saldo() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    total NUMERIC;
BEGIN
    -- Soma depósitos e saques para o usuário
    SELECT COALESCE(SUM(valor),0) INTO total 
    FROM transacoes 
    WHERE usuario_id = NEW.usuario_id;

    INSERT INTO monetaria_historico(usuario_id, saldo, data_atualizacao)
    VALUES (NEW.usuario_id, total, NOW());

    RETURN NEW;
END;
$$;


ALTER FUNCTION public.atualiza_saldo() OWNER TO postgres;

--
-- Name: insere_transacao_aposta_approved(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.insere_transacao_aposta_approved() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NEW.status = 'approved' THEN
        INSERT INTO transacoes (usuario_id, aposta_id, tipo, valor)
        VALUES (NEW.usuario_id, NEW.id, 'aposta', NEW.valor);
    END IF;
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.insere_transacao_aposta_approved() OWNER TO postgres;

--
-- Name: insere_transacao_approved(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.insere_transacao_approved() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Dispara apenas quando o status é 'approved'
    IF NEW.status = 'approved' THEN
        -- Evita duplicar transação se já existir uma para o mesmo pagamento
        IF NOT EXISTS (
            SELECT 1 FROM transacoes WHERE pagamento_id = NEW.payment_id
        ) THEN
            INSERT INTO transacoes (usuario_id, pagamento_id, tipo, valor)
            VALUES (NEW.usuario_id, NEW.payment_id, 'deposito', NEW.valor);
        END IF;
    END IF;

    RETURN NEW;
END;
$$;


ALTER FUNCTION public.insere_transacao_approved() OWNER TO postgres;

--
-- Name: trg_aposta_approved(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.trg_aposta_approved() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF NEW.status = 'approved' AND OLD.status IS DISTINCT FROM 'approved' THEN
    -- Exemplo: atualiza data de aprovação
    NEW.data_aprovado := NOW();

    -- Aqui pode vir a lógica que você quiser:
    -- INSERT INTO monetaria(usuario_id, valor, tipo) VALUES (NEW.usuario_id, -NEW.valor, 'aposta');
    RAISE NOTICE 'Aposta % aprovada para o usuário % no valor de %', NEW.id, NEW.usuario_id, NEW.valor;
  END IF;

  RETURN NEW;
END;
$$;


ALTER FUNCTION public.trg_aposta_approved() OWNER TO postgres;

--
-- Name: trg_aposta_insert(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.trg_aposta_insert() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  RAISE NOTICE 'Nova aposta criada para usuário %, status: %', NEW.usuario_id, NEW.status;
  RETURN NEW;
END;
$$;


ALTER FUNCTION public.trg_aposta_insert() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: apostas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.apostas (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    status text DEFAULT 'pending'::text NOT NULL,
    valor numeric(10,2) NOT NULL,
    data_criacao timestamp without time zone DEFAULT now(),
    data_aprovado timestamp without time zone
);


ALTER TABLE public.apostas OWNER TO postgres;

--
-- Name: apostas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.apostas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.apostas_id_seq OWNER TO postgres;

--
-- Name: apostas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.apostas_id_seq OWNED BY public.apostas.id;


--
-- Name: monetaria_historico; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.monetaria_historico (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    saldo numeric(12,2) NOT NULL,
    data_atualizacao timestamp without time zone DEFAULT now()
);


ALTER TABLE public.monetaria_historico OWNER TO postgres;

--
-- Name: monetaria_historico_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.monetaria_historico_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.monetaria_historico_id_seq OWNER TO postgres;

--
-- Name: monetaria_historico_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.monetaria_historico_id_seq OWNED BY public.monetaria_historico.id;


--
-- Name: pagamentos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pagamentos (
    id bigint NOT NULL,
    usuario_id integer NOT NULL,
    payment_id bigint NOT NULL,
    status character varying(20) NOT NULL,
    valor numeric(12,2) NOT NULL,
    data_recebimento timestamp without time zone DEFAULT now(),
    payload jsonb
);


ALTER TABLE public.pagamentos OWNER TO postgres;

--
-- Name: pagamentos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pagamentos_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pagamentos_id_seq OWNER TO postgres;

--
-- Name: pagamentos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pagamentos_id_seq OWNED BY public.pagamentos.id;


--
-- Name: roleta; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roleta (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    aposta_id bigint NOT NULL,
    cor_cliente character varying(8) NOT NULL,
    cor_server character varying(8) NOT NULL,
    resultado boolean,
    data_criacao timestamp without time zone DEFAULT now(),
    CONSTRAINT roleta_cor_cliente_check CHECK (((cor_cliente)::text = ANY ((ARRAY['B'::character varying, 'R'::character varying, 'W'::character varying, 'black'::character varying, 'red'::character varying, 'white'::character varying, 'preto'::character varying, 'vermelho'::character varying, 'branco'::character varying])::text[]))),
    CONSTRAINT roleta_cor_server_check CHECK (((cor_server)::text = ANY ((ARRAY['B'::character varying, 'R'::character varying, 'W'::character varying, 'black'::character varying, 'red'::character varying, 'white'::character varying, 'preto'::character varying, 'vermelho'::character varying, 'branco'::character varying])::text[])))
);


ALTER TABLE public.roleta OWNER TO postgres;

--
-- Name: roleta_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roleta_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.roleta_id_seq OWNER TO postgres;

--
-- Name: roleta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roleta_id_seq OWNED BY public.roleta.id;


--
-- Name: saldo_atual; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.saldo_atual AS
 SELECT DISTINCT ON (monetaria_historico.usuario_id) monetaria_historico.usuario_id,
    monetaria_historico.saldo,
    monetaria_historico.data_atualizacao
   FROM public.monetaria_historico
  ORDER BY monetaria_historico.usuario_id, monetaria_historico.data_atualizacao DESC;


ALTER TABLE public.saldo_atual OWNER TO postgres;

--
-- Name: transacoes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transacoes (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    pagamento_id bigint,
    tipo character varying(10) NOT NULL,
    valor numeric(12,2) NOT NULL,
    data_transacao timestamp without time zone DEFAULT now(),
    aposta_id bigint
);


ALTER TABLE public.transacoes OWNER TO postgres;

--
-- Name: transacoes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.transacoes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.transacoes_id_seq OWNER TO postgres;

--
-- Name: transacoes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.transacoes_id_seq OWNED BY public.transacoes.id;


--
-- Name: usuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuario (
    id integer NOT NULL,
    nome character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    senha character varying(100) NOT NULL
);


ALTER TABLE public.usuario OWNER TO postgres;

--
-- Name: usuario_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuario_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.usuario_id_seq OWNER TO postgres;

--
-- Name: usuario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuario_id_seq OWNED BY public.usuario.id;


--
-- Name: webhook_failures; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.webhook_failures (
    id integer NOT NULL,
    payment_id bigint,
    status character varying(20),
    payload jsonb,
    error_message text,
    date_created timestamp without time zone DEFAULT now()
);


ALTER TABLE public.webhook_failures OWNER TO postgres;

--
-- Name: webhook_failures_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.webhook_failures_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.webhook_failures_id_seq OWNER TO postgres;

--
-- Name: webhook_failures_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.webhook_failures_id_seq OWNED BY public.webhook_failures.id;


--
-- Name: apostas id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.apostas ALTER COLUMN id SET DEFAULT nextval('public.apostas_id_seq'::regclass);


--
-- Name: monetaria_historico id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.monetaria_historico ALTER COLUMN id SET DEFAULT nextval('public.monetaria_historico_id_seq'::regclass);


--
-- Name: pagamentos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pagamentos ALTER COLUMN id SET DEFAULT nextval('public.pagamentos_id_seq'::regclass);


--
-- Name: roleta id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roleta ALTER COLUMN id SET DEFAULT nextval('public.roleta_id_seq'::regclass);


--
-- Name: transacoes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transacoes ALTER COLUMN id SET DEFAULT nextval('public.transacoes_id_seq'::regclass);


--
-- Name: usuario id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario ALTER COLUMN id SET DEFAULT nextval('public.usuario_id_seq'::regclass);


--
-- Name: webhook_failures id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.webhook_failures ALTER COLUMN id SET DEFAULT nextval('public.webhook_failures_id_seq'::regclass);


--
-- Name: apostas apostas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.apostas
    ADD CONSTRAINT apostas_pkey PRIMARY KEY (id);


--
-- Name: monetaria_historico monetaria_historico_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.monetaria_historico
    ADD CONSTRAINT monetaria_historico_pkey PRIMARY KEY (id);


--
-- Name: pagamentos pagamentos_payment_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pagamentos
    ADD CONSTRAINT pagamentos_payment_id_key UNIQUE (payment_id);


--
-- Name: pagamentos pagamentos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pagamentos
    ADD CONSTRAINT pagamentos_pkey PRIMARY KEY (id);


--
-- Name: roleta roleta_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roleta
    ADD CONSTRAINT roleta_pkey PRIMARY KEY (id);


--
-- Name: transacoes transacoes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transacoes
    ADD CONSTRAINT transacoes_pkey PRIMARY KEY (id);


--
-- Name: usuario usuario_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_email_key UNIQUE (email);


--
-- Name: usuario usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id);


--
-- Name: webhook_failures webhook_failures_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.webhook_failures
    ADD CONSTRAINT webhook_failures_pkey PRIMARY KEY (id);


--
-- Name: apostas trg_apostas_after_insert; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_apostas_after_insert AFTER INSERT ON public.apostas FOR EACH ROW EXECUTE FUNCTION public.insere_transacao_aposta_approved();


--
-- Name: apostas trg_apostas_after_update; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_apostas_after_update AFTER UPDATE ON public.apostas FOR EACH ROW EXECUTE FUNCTION public.insere_transacao_aposta_approved();


--
-- Name: pagamentos trg_pagamentos_after_insert; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_pagamentos_after_insert AFTER INSERT ON public.pagamentos FOR EACH ROW EXECUTE FUNCTION public.insere_transacao_approved();


--
-- Name: pagamentos trg_pagamentos_after_update; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_pagamentos_after_update AFTER UPDATE OF status ON public.pagamentos FOR EACH ROW WHEN ((((new.status)::text = 'approved'::text) AND ((old.status)::text IS DISTINCT FROM 'approved'::text))) EXECUTE FUNCTION public.insere_transacao_approved();


--
-- Name: transacoes trg_transacoes_after_insert; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_transacoes_after_insert AFTER INSERT ON public.transacoes FOR EACH ROW EXECUTE FUNCTION public.atualiza_saldo();


--
-- Name: apostas apostas_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.apostas
    ADD CONSTRAINT apostas_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuario(id);


--
-- Name: monetaria_historico monetaria_historico_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.monetaria_historico
    ADD CONSTRAINT monetaria_historico_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuario(id);


--
-- Name: pagamentos pagamentos_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pagamentos
    ADD CONSTRAINT pagamentos_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuario(id);


--
-- Name: roleta roleta_aposta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roleta
    ADD CONSTRAINT roleta_aposta_id_fkey FOREIGN KEY (aposta_id) REFERENCES public.apostas(id);


--
-- Name: roleta roleta_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roleta
    ADD CONSTRAINT roleta_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuario(id);


--
-- Name: transacoes transacoes_pagamento_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transacoes
    ADD CONSTRAINT transacoes_pagamento_id_fkey FOREIGN KEY (pagamento_id) REFERENCES public.pagamentos(payment_id);


--
-- Name: transacoes transacoes_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transacoes
    ADD CONSTRAINT transacoes_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuario(id);


--
-- PostgreSQL database dump complete
--

