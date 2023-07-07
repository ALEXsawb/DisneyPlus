from typing import List, Literal

from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

from backend.models.UserModel import UserModel
from backend.schemas import User
from backend.schemas import Visit

admin = APIRouter(prefix='/admin')
SORT_TYPES_USER_DATA = Literal['email', 'password', 'visits', 'admin']


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_personal_data(self, data: dict | List[dict] | list, websocket: WebSocket):
        await websocket.send_json(data)

    async def broadcast(self, data=None):
        for connection in self.active_connections:
            await connection.send_json(data)


manager = ConnectionManager()


async def broadcast_visit(data: Visit):
    await manager.broadcast({**data.dict(), 'event': 'add_visit'})


async def broadcast_user(data: User):
    await manager.broadcast({**data.dict(), 'event': 'add_user'})


@admin.websocket('/ws/users')
async def get_user_data(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        first_ten_users_without_visits = await UserModel.get_users()
        await manager.send_personal_data({'data': first_ten_users_without_visits,
                                          'count_users': await UserModel.get_documents_count(),
                                          'event': 'connect'},
                                         websocket)
        while True:
            data = await websocket.receive_json()
            match data['event']:
                case 'show_more_visits':
                    if 'limit' in data:
                        visits = await UserModel.get_visits(data['user_id'], limit=data['limit'], skip=data['count'])
                    else:
                        visits = await UserModel.get_visits(data['user_id'], skip=data['count'])
                    visits['user_id'] = data['user_id']
                    visits['event'] = 'add_visits'
                    await manager.send_personal_data(visits, websocket)
                case 'show_more_users':
                    if 'limit' in data:
                        users = await UserModel.get_users(users_limit=data['limit'], skip=data['count'])
                    else:
                        users = await UserModel.get_users(skip=data['count'])
                    await manager.send_personal_data({'event': 'add_users', 'users': users}, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client left the chat")