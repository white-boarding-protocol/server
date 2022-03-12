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
            return await self._create_room()
        elif self.type == RoomEventType.END_ROOM:
            return await self._end_room()
        elif self.type == RoomEventType.USER_JOIN:
            return await self._enter_room()
        elif self.type == RoomEventType.USER_LEAVE:
            return await self._leave_room()
        elif self.type == RoomEventType.ACCEPT_JOIN:
            return await self._accept_join()
        elif self.type == RoomEventType.DECLINE_JOIN:
            return await self._decline_join()

    def is_valid(self) -> bool:
        if self.type != RoomEventType.CREATE_ROOM and self.room_id is None:
            self.error_msg = "room_id parameter is missing in the payload"
            return False
        if self.type in [RoomEventType.ACCEPT_JOIN, RoomEventType.DECLINE_JOIN] and self.target_user is None:
            self.error_msg = "target_user is missing in the payload"
            return False
        return True

    async def handle_error(self):
        await self.client_socket.send(json.dumps({"message": self.error_msg, "status": 400}))

    async def _create_room(self) -> list:
        self.room_id = self.whiteboarding.redis_connector.create_room(self.user_id)
        self.whiteboarding.redis_connector.insert_user(self.room_id, self.user_id)
        await self.client_socket.send(json.dumps({"status": 201, "message": "room created"}))
        return []

    async def _end_room(self) -> list:
        pass

    async def _leave_room(self) -> list:
        pass

    async def _accept_join(self) -> list:
        self.whiteboarding.redis_connector.insert_user(self.room_id, self.target_user)
        room_events = self.whiteboarding.redis_connector.get_events(self.room_id)
        await self.client_socket.send({"status": 200, "events": room_events})
        # TODO not done
        return []

    async def _decline_join(self) -> list:
        pass

    async def _enter_room(self) -> list:
        host_id = self.whiteboarding.redis_connector.get_host(self.room_id)
        host_socket = self.whiteboarding.get_client_socket(host_id)
        host_socket.send()
        return [host_id]
