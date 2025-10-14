const { verifyToken } = require('../utils/token');

function authMiddleware(req, res, next) {
  const authHeader = req.headers['authorization'];

  if (!authHeader) return res.status(401).json({ message: 'Token não fornecido' });

  const token = authHeader.split(' ')[1];
  if (!token) return res.status(401).json({ message: 'Token inválido' });

  try {
    const decoded = verifyToken(token);
    console.log(decoded);
    req.userId = decoded.id; // armazena dados do usuário no request
    console.log(req.userId);
    next();
  } catch (err) {
    return res.status(403).json({ message: 'Token inválido ou expirado' });
  }
}

module.exports = authMiddleware;
