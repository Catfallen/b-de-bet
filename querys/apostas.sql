/*
exemplo de insert e update
CREATE TABLE apostas (
  id SERIAL PRIMARY KEY,
  usuario_id INTEGER NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending',
  valor NUMERIC(10,2) NOT NULL,
  data_criacao TIMESTAMP DEFAULT NOW(),
  data_aprovado TIMESTAMP,
  foreign KEY(usuario_id) references usuario(id)
);
*/

-- =========================================
-- FUNÇÃO: INSERIR TRANSACAO AUTOMATICA PARA APROVADAS
-- =========================================
-- =========================================
-- FUNÇÃO: INSERIR TRANSACAO AUTOMATICA PARA APOSTAS APROVADAS
-- =========================================
CREATE OR REPLACE FUNCTION insere_transacao_aposta_approved()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'approved' THEN
        INSERT INTO transacoes (usuario_id, payment_id, tipo, valor)
        VALUES (NEW.usuario_id, NEW.id, 'aposta', NEW.valor);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- TRIGGER: após INSERT na tabela apostas
CREATE TRIGGER trg_apostas_after_insert
AFTER INSERT ON apostas
FOR EACH ROW
EXECUTE FUNCTION insere_transacao_aposta_approved();

-- TRIGGER: após UPDATE da coluna status para 'approved'
CREATE TRIGGER trg_apostas_after_update
AFTER UPDATE OF status ON apostas
FOR EACH ROW
WHEN (NEW.status = 'approved' AND OLD.status IS DISTINCT FROM 'approved')
EXECUTE FUNCTION insere_transacao_aposta_approved();