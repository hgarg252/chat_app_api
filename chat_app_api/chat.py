import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from database import Users, get_db,Messages
from auth import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/websockets", tags=["Websockets"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, username: str, websocket: WebSocket):
        await websocket.accept()
        if username not in self.active_connections:
            self.active_connections[username] = []
        self.active_connections[username].append(websocket)

    def disconnect(self, username: str, websocket: WebSocket):
        if username in self.active_connections:
            self.active_connections[username].remove(websocket)
            if not self.active_connections[username]:  # cleanup if empty
                self.active_connections.pop(username)

    async def send_message(self, message: str, to_user: str, db: Session):
        user = db.query(Users).filter(Users.email == to_user).first()
        if not user:
            return
        if to_user not in self.active_connections:
            return
        # Send to all active connections of the user
        for ws in self.active_connections[to_user]:
            await ws.send_text(message)


manager = ConnectionManager()

@router.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            await websocket.close(code=1008)
            return
        user = db.query(Users).filter(Users.email == username).first()
        if not user:
            await websocket.close(code=1008)
            return
    except JWTError:
        await websocket.close(code=1008)
        return
    await manager.connect(user.email, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            try:
                message_data = json.loads(data)
                to_user = message_data.get("to")
                msg = message_data.get("message")
                if not to_user or not msg:
                    await websocket.send_text(json.dumps({"error": "Missing 'to' or 'message'"}))
                    continue
                check_user=db.query(Users).filter(Users.email==to_user).first()
                if not check_user:
                    await websocket.send_text(json.dumps({"error":f"User with id {to_user} does not exists"}))
                    continue
                if not to_user in manager.active_connections:
                    await websocket.send_text(json.dumps({"error": f"User {to_user} is offline"}))
                    continue
                await manager.send_message(f"{user.name} : {msg}", to_user, db)
                new_message=Messages(sender=user.email,receiver=to_user,message_content=msg,sender_id=user.id)
                db.add(new_message)
                db.commit()
                db.refresh(new_message)
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({"error": "Invalid JSON format"}))
    except WebSocketDisconnect:
        manager.disconnect(user.email)
