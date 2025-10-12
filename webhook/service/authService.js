const { pool } = require('../config/db');
const { hashPassword, comparePassword } = require('../utils/hash');
const { generateToken } = require('../utils/token');

async function register({ nome, email, senha }) {
  // 1️⃣ Hash da senha
  const hashed = await hashPassword(senha);

  // 2️⃣ Inserir no banco
  const query = `
    INSERT INTO usuario (nome, email, senha)
    VALUES ($1, $2, $3)
    RETURNING id, nome, email
  `;
  const { rows } = await pool.query(query, [nome, email, hashed]);
  const user = rows[0];

  // 3️⃣ Gerar token JWT
  const token = generateToken({ id: user.id, email: user.email });

  // 4️⃣ Retornar usuário + token
  return { user, token };
}


async function login({ email, senha }) {
  const query = 'SELECT * FROM usuario WHERE email = $1';
  const { rows } = await pool.query(query, [email]);
  const user = rows[0];

  if (!user) throw new Error('Usuário não encontrado');

  const valid = await comparePassword(senha, user.senha);
  if (!valid) throw new Error('Senha incorreta');

  const token = generateToken({ id: user.id, email: user.email });
  return { token, user: { id: user.id, email: user.email } };
}

module.exports = { register, login };
