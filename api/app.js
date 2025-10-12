const express = require('express');
const app = express();
const authRoutes = require('./routes/authRoutes');
const cors = require('cors')
app.use(express.json());
app.use(cors());
app.use('/auth', authRoutes);
cors();
const PORT = 3000;
app.listen(PORT, () => console.log(`Servidor rodando na porta ${PORT}`));
