from fastapi import FastAPI, WebSocket

app = FastAPI()
clients = []

@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            for client in clients:
                if client != websocket:
                    await client.send_text(data)
    except:
        clients.remove(websocket)
