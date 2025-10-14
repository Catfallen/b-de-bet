

-- =========================================
-- TABELA DE PAGAMENTOS (WEBHOOK HISTÓRICO)
-- =========================================
CREATE TABLE pagamentos (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuario(id),
    payment_id VARCHAR(100) NOT NULL UNIQUE,
    status VARCHAR(20) NOT NULL, -- approved, rejected, pending, cancelled
    valor NUMERIC(12,2) NOT NULL,
    data_recebimento TIMESTAMP DEFAULT NOW(),
    payload JSONB
);

-- =========================================
-- TABELA DE TRANSACOES FINANCEIRAS
-- =========================================
CREATE TABLE transacoes (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuario(id),
    pagamento_id VARCHAR(100) REFERENCES pagamentos(payment_id),
    tipo VARCHAR(10) NOT NULL, -- 'deposito' ou 'saque'
    valor NUMERIC(12,2) NOT NULL,
    data_transacao TIMESTAMP DEFAULT NOW()
);

-- =========================================
-- TABELA DE SALDO (HISTORICO)
-- =========================================
CREATE TABLE monetaria_historico (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuario(id),
    saldo NUMERIC(12,2) NOT NULL,
    data_atualizacao TIMESTAMP DEFAULT NOW()
);

-- =========================================
-- TRIGGER PARA INSERIR TRANSACAO AUTOMATICA APENAS PARA PAGAMENTOS APROVADOS
-- =========================================
CREATE OR REPLACE FUNCTION insere_transacao_approved()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'approved' THEN
        INSERT INTO transacoes (usuario_id, pagamento_id, tipo, valor)
        VALUES (NEW.usuario_id, NEW.payment_id, 'deposito', NEW.valor);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_pagamentos_after_insert
AFTER INSERT ON pagamentos
FOR EACH ROW
EXECUTE FUNCTION insere_transacao_approved();

-- =========================================
-- TRIGGER PARA ATUALIZAR SALDO AUTOMATICAMENTE
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

-- =========================================
-- OBSERVAÇÕES:
-- 1. Somente pagamentos aprovados geram transações automaticamente.
-- 2. Saques devem ser inseridos manualmente na tabela transacoes com tipo = 'saque' e valor negativo.
-- 3. A tabela monetaria_historico mantém o histórico de saldo por usuário.
-- 4. Para checar saldo atual, pegar o último registro da tabela monetaria_historico para cada usuário:
--    SELECT saldo FROM monetaria_historico WHERE usuario_id = X ORDER BY data_atualizacao DESC LIMIT 1;

CREATE TABLE webhook_failures (
    id SERIAL PRIMARY KEY,
    payment_id VARCHAR(100),
    status VARCHAR(20),
    payload JSONB,
    error_message TEXT,
    date_created TIMESTAMP DEFAULT NOW()
);
