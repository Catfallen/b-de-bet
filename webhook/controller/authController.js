const authService = require('../service/authService');

async function register(req, res) {
  try {
    const { nome,email, senha } = req.body; //body da requisição
    console.log(req.body); //teste
    const user = await authService.register({ nome,email, senha }); //chamada do service
    return res.status(201).json(user);
  } catch (err) {
    return res.status(400).json({ error: err.message });
  }
}

async function login(req, res) {
  try {
    const { email, senha } = req.body;
    const result = await authService.login({ email, senha });
    return res.status(200).json(result);
  } catch (err) {
    return res.status(400).json({ error: err.message });
  }
}

async function protectedRoute(req, res) {
  return res.status(403).json({ message: `Bem-vindo, ${req.user.email}!`, user: req.user });
}

module.exports = { register, login, protectedRoute };
