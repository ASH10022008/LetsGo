from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
import json

app = FastAPI(title="Live Campus Transit API", version="1.0")

# Enable CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connection Manager to keep track of active student WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_student_connections: List[WebSocket] = []

    async def connect_student(self, websocket: WebSocket):
        await websocket.accept()
        self.active_student_connections.append(websocket)

    def disconnect_student(self, websocket: WebSocket):
        self.active_student_connections.remove(websocket)

    async def broadcast_to_students(self, message: str):
        for connection in self.active_student_connections:
            try:
                await connection.send_text(message)
            except Exception:
                # Handle dead sockets gracefully
                pass

manager = ConnectionManager()

@app.get("/")
def read_root():
    return {"status": "Campus Transit Backend is running successfully!"}

# Driver WebSocket endpoint: receives location updates
@app.websocket("/ws/driver/{bus_id}")
async def driver_websocket(websocket: WebSocket, bus_id: str):
    await websocket.accept()
    print(f"Driver connected for Bus ID: {bus_id}")
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            
            # Enrich payload with mock stop details for the student UI preview
            payload["next_stop"] = "Central Library Gate"
            payload["last_stop"] = "Hostel Block B"
            payload["eta"] = "4 mins"

            # Broadcast the updated telemetry to all connected students
            await manager.broadcast_to_students(json.dumps(payload))
            
    except WebSocketDisconnect:
        print(f"Driver disconnected for Bus ID: {bus_id}")

# Student WebSocket endpoint: streams live bus locations
@app.websocket("/ws/student")
async def student_websocket(websocket: WebSocket):
    await manager.connect_student(websocket)
    print("Student client connected.")
    try:
        while True:
            # Keep connection alive waiting for incoming client frames (if any)
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect_student(websocket)
        print("Student client disconnected.")