import json

from events.masterevent import MasterEvent
from events.room.constants import RoomEventType


class RoomEvent(MasterEvent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = kwargs.get("room_event_type")
        self.target_user = kwargs.get("target_user")
        self.error_msg = None

    def to_dict(self) -> dict:
        parent = super().to_dict()
        parent["type"] = self.type
        parent["target_user"] = self.target_user
        return parent

    def has_perm(self) -> bool:
        if self.type in [RoomEventType.CREATE_ROOM, RoomEventType.USER_JOIN, RoomEventType.USER_LEAVE]:
            return True
        if self.type in [RoomEventType.ACCEPT_JOIN, RoomEventType.DECLINE_JOIN, RoomEventType.END_ROOM]:
            return self.is_user_host

    async def handle(self) -> list:
        if self.type == RoomEventType.CREATE_ROOM:
            pass
        elif self.type == RoomEventType.END_ROOM:
            pass
        elif self.type == RoomEventType.USER_JOIN:
            pass
        elif self.type == RoomEventType.USER_LEAVE:
            pass
        elif self.type == RoomEventType.ACCEPT_JOIN:
            pass
        elif self.type == RoomEventType.DECLINE_JOIN:
            pass
        return []

    def is_valid(self) -> bool:
        if self.type != RoomEventType.CREATE_ROOM and self.room_id is None:
            self.error_msg = "room_id parameter is missing in the payload"
            return False
        return True

    async def handle_error(self):
        await self.client_socket.send(json.dumps({"message": self.error_msg, "status": 400}))
