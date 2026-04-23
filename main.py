from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()
clients = []

@app.on_event("startup")
async def show_routes():
    print("=== ROUTES LOADED ===")
    for route in app.routes:
        print(type(route).__name__, getattr(route, "path", None))

@app.get("/")
def home():
    return {"status": "server online"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    print("WebSocket client connected")

    try:
        while True:
            data = await websocket.receive_text()
            print("Received:", data)

            for client in clients[:]:
                if client != websocket:
                    try:
                        await client.send_text(data)
                    except Exception:
                        if client in clients:
                            clients.remove(client)

    except WebSocketDisconnect:
        print("WebSocket disconnected")
        if websocket in clients:
            clients.remove(websocket)
    except Exception as e:
        print("WebSocket error:", e)
        if websocket in clients:
            clients.remove(websocket)
