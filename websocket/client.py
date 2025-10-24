import asyncio
import websockets
import json

async def play():
    async with websockets.connect("ws://localhost:8080") as ws:
        # envia uma jogada
        await ws.send(json.dumps({"type": "abrir_celula", "row": 2, "col": 3}))
        
        # espera resposta do servidor
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            print("Servidor disse:", data)

asyncio.run(play())
