const { WebSocketServer } = require('ws');

const wss = new WebSocketServer({ port: 8080 });

wss.on('connection', (socket) => {
    socket.on('message', (msg) => {
        const data = JSON.parse(msg);
        if (data.type === 'abrir_celula') {
            const resposta = { type: 'resultado', boom: false, adjacent: 2 };
            socket.send(JSON.stringify(resposta));
        }
    });
    // Exemplo de push automático do servidor
    setTimeout(() => {
        socket.send(JSON.stringify({ type: 'saldo_atualizado', saldo: 95.0 }));
    }, 3000);
});