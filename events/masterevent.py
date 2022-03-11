import json
from abc import abstractmethod
from time import time

from events.constants import EventType
from whiteboarding.whiteboarding import Whiteboarding


class MasterEvent:
    CONNECT_MSG = "hello"
    DISCONNECT_MSG = "fin"

    def __init__(self, **kwargs):
        self.user_id = kwargs.get("user_id")
        self.room_id = kwargs.get("room_id")
        self.message = kwargs.get("message")
        self.client_socket = kwargs.get("client_socket")

        if kwargs.get("time_stamp"):
            self.time_stamp = kwargs.get("time_stamp")
        else:
            self.time_stamp = time()

        self.whiteboarding = Whiteboarding()
        self._room_users = None

    @property
    def room_users(self):
        if self._room_users is None:
            self._room_users = self.whiteboarding.redis_connector.get_users(self.room_id)
        return self._room_users

    @abstractmethod
    def has_perm(self) -> bool:
        pass

    @abstractmethod
    async def handle(self) -> list:
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    async def handle_error(self):
        pass

    async def exec(self) -> bool:
        continue_connection = True
        if self.user_id is None:
            await self.client_socket.send(json.dumps({"message": "user_id is a required field", "status": 400}))

        if not self.whiteboarding.is_client_registered(self.user_id):
            if self.message == self.CONNECT_MSG:
                await self._register_user()
            else:
                continue_connection = False
        else:
            if self.message == self.DISCONNECT_MSG:
                await self._unregister_user()
                continue_connection = False
            else:
                if self.has_perm():
                    if self.is_valid():
                        redistribute_to = await self.handle()
                        await self._redistribute(redistribute_to)
                    else:
                        await self.handle_error()
                else:
                    await self.client_socket.send(
                        json.dumps({"message": "user cannot perform this action", "status": 403}))

        return continue_connection

    async def _register_user(self):
        self.whiteboarding.add_online_user(self.user_id, self.client_socket)
        await self.client_socket.send({"message": "connected", "status": 200})

    async def _unregister_user(self):
        self.whiteboarding.remove_online_user(self.user_id)
        await self.client_socket.send({"message": "disconnected", "status": 200})

    @staticmethod
    def deserialize(data, client_socket):
        data["client_socket"] = client_socket

        event_type = data.get("type")
        if event_type is None:
            return MasterEvent(**data)

        data.pop("type")
        if event_type == EventType.ROOM:
            from events.room.room_event import RoomEvent
            return RoomEvent(**data)
        elif event_type == EventType.DRAW:
            from events.whiteboard.draw import DrawWhiteboardEvent
            return DrawWhiteboardEvent(**data)
        elif event_type == EventType.STICKY_NOTE:
            from events.whiteboard.sticky_note import StickyNoteWhiteboardEvent
            return StickyNoteWhiteboardEvent(**data)
        elif event_type == EventType.IMAGE:
            from events.whiteboard.image import ImageWhiteboardEvent
            return ImageWhiteboardEvent(**data)
        elif event_type == EventType.UNDO:
            from events.whiteboard.undo import UndoWhiteboardEvent
            return UndoWhiteboardEvent(**data)

    async def _redistribute(self, redistribute_to: list):
        event_json = json.dumps(self.to_dict())
        for user_id in redistribute_to:
            user_socket = self.whiteboarding.get_client_socket(user_id)
            await user_socket.send(json.dumps(event_json))

    def to_dict(self) -> dict:
        return {
            "message": self.message,
            "user_id": self.user_id,
            "room_id": self.room_id,
            "time_stamp": self.time_stamp
        }
