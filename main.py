from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()
clients = []

@app.get("/")
def home():
    return {"status": "server online"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()

            for client in clients[:]:
                if client != websocket:
                    try:
                        await client.send_text(data)
                    except Exception:
                        if client in clients:
                            clients.remove(client)

    except WebSocketDisconnect:
        if websocket in clients:
            clients.remove(websocket)
    except Exception:
        if websocket in clients:
            clients.remove(websocket)
