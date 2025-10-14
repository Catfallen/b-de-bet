-- =========================================
-- TABELA DE USUÁRIOS (exemplo)
-- =========================================
CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(100) NOT NULL
);

-- =========================================
-- TABELA DE PAGAMENTOS (WEBHOOK HISTÓRICO)
-- =========================================
CREATE TABLE pagamentos (
    id BIGSERIAL PRIMARY KEY,
    payment_id BIGINT NOT NULL UNIQUE,
    status VARCHAR(20) NOT NULL, -- approved, rejected, pending, cancelled
    valor NUMERIC(12,2) NOT NULL,
    data_recebimento TIMESTAMP DEFAULT NOW(),
    payload JSONB
);

-- =========================================
-- TABELA DE PAGAMENTO_USUARIO (para mapear pagamentos a usuários)
-- =========================================
CREATE TABLE pagamento_usuario (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuario(id),
    pagamento_id BIGINT NOT NULL REFERENCES pagamentos(payment_id),
    UNIQUE(usuario_id, pagamento_id)
);

-- =========================================
-- TABELA DE TRANSACOES FINANCEIRAS
-- =========================================
CREATE TABLE transacoes (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuario(id),
    pagamento_id BIGINT REFERENCES pagamentos(payment_id),
    tipo VARCHAR(10) NOT NULL, -- 'deposito' ou 'saque'
    valor NUMERIC(12,2) NOT NULL,
    data_transacao TIMESTAMP DEFAULT NOW()
);

-- =========================================
-- TABELA DE SALDO (HISTÓRICO)
-- =========================================
CREATE TABLE monetaria_historico (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuario(id),
    saldo NUMERIC(12,2) NOT NULL,
    data_atualizacao TIMESTAMP DEFAULT NOW()
);

-- =========================================
-- TABELA DE WEBHOOK FAILURES
-- =========================================
CREATE TABLE webhook_failures (
    id SERIAL PRIMARY KEY,
    payment_id BIGINT,
    status VARCHAR(20),
    payload JSONB,
    error_message TEXT,
    date_created TIMESTAMP DEFAULT NOW()
);

-- =========================================
-- TRIGGER: INSERIR TRANSACAO AUTOMATICA APENAS PARA PAGAMENTOS APROVADOS
-- =========================================
CREATE OR REPLACE FUNCTION insere_transacao_approved()
RETURNS TRIGGER AS $$
DECLARE
    usuario INT;
BEGIN
    -- Busca o usuario_id a partir da tabela pagamento_usuario
    SELECT usuario_id INTO usuario 
    FROM pagamento_usuario
    WHERE pagamento_id = NEW.payment_id;

    IF usuario IS NULL THEN
        RAISE NOTICE 'Pagamento % não possui usuário associado', NEW.payment_id;
        RETURN NEW;
    END IF;

    IF NEW.status = 'approved' THEN
        INSERT INTO transacoes (usuario_id, pagamento_id, tipo, valor)
        VALUES (usuario, NEW.payment_id, 'deposito', NEW.valor);
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_pagamentos_after_insert
AFTER INSERT ON pagamentos
FOR EACH ROW
EXECUTE FUNCTION insere_transacao_approved();

-- =========================================
-- TRIGGER: ATUALIZAR SALDO AUTOMATICAMENTE
-- =========================================
CREATE OR REPLACE FUNCTION atualiza_saldo()
RETURNS TRIGGER AS $$
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
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_transacoes_after_insert
AFTER INSERT ON transacoes
FOR EACH ROW
EXECUTE FUNCTION atualiza_saldo();