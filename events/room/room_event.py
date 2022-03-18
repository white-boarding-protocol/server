import json

from events.constants import UserStatus
from events.masterevent import MasterEvent
from events.room.constants import RoomEventType


class RoomEvent(MasterEvent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = kwargs.get("room_event_type")
        self.target_user_id = kwargs.get("target_user_id")
        self.error_msg = None

    def to_dict(self) -> dict:
        parent = super().to_dict()
        parent["type"] = self.type
        parent["target_user_id"] = self.target_user_id
        return parent

    def has_perm(self) -> bool:
        if self.type in [RoomEventType.CREATE_ROOM, RoomEventType.USER_JOIN, RoomEventType.USER_LEAVE]:
            return True
        if self.type in [RoomEventType.ACCEPT_JOIN, RoomEventType.DECLINE_JOIN, RoomEventType.END_ROOM]:
            return self.is_user_host

    async def handle(self):
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
        if self.type in [RoomEventType.ACCEPT_JOIN, RoomEventType.DECLINE_JOIN] and self.target_user_id is None:
            self.error_msg = "target_user is missing in the payload"
            return False
        return True

    async def _create_room(self):
        self.room_id = self.whiteboarding.redis_connector.create_room(self.user_id)
        user = self.whiteboarding.redis_connector.get_user(self.user_id)
        user["status"] = UserStatus.IN_ROOM
        user["room_id"] = self.room_id
        self.whiteboarding.redis_connector.update_user(self.user_id, user)
        self.whiteboarding.redis_connector.insert_user(self.room_id, self.user_id)
        await self.client_socket.send(
            json.dumps({"status": 200, "message": "room created", "room_id": self.room_id, "uuid": self.uuid}))

    async def _end_room(self):
        room_users = self.room_users
        for user in room_users:
            user["state"] = UserStatus.OUT_ROOM
            user["room_id"] = None
            self.whiteboarding.redis_connector.update_user(user.get("id"), user)

        self.whiteboarding.redis_connector.remove_room(self.room_id)
        await self.client_socket.send(json.dumps({"status": 200, "message": "room ended", "uuid": self.uuid}))
        await self.redistribute([x.get("id") for x in room_users])

    async def _leave_room(self):
        self.whiteboarding.redis_connector.remove_user_from_room(self.room_id, self.user_id)
        current_user_data = self.whiteboarding.redis_connector.get_user(self.user_id)
        current_user_data["state"] = UserStatus.OUT_ROOM
        current_user_data["room_id"] = None
        self.whiteboarding.redis_connector.update_user(self.user_id, current_user_data)
        await self.client_socket.send(json.dumps({"status": 200, "message": "left room", "uuid": self.uuid}))
        await self.redistribute([x.get("id") for x in self.room_users])

    async def _accept_join(self):
        user = self.whiteboarding.redis_connector.get_user(self.target_user_id)
        user["status"] = UserStatus.IN_ROOM
        self.whiteboarding.redis_connector.update_user(self.target_user_id, user)

        self.whiteboarding.redis_connector.insert_user(self.room_id, self.target_user_id)
        room_events = self.whiteboarding.redis_connector.get_room_events(self.room_id)
        user_socket = self.whiteboarding.get_client_socket(self.target_user_id)
        await user_socket.send(json.dumps(
            {"status": 302, "message": "accepted", "room_id": self.room_id, "events": room_events}))

        await self.client_socket.send(json.dumps({"status": 200, "message": "user accepted", "uuid": self.uuid}))
        await self.redistribute([x.get("id") for x in self.room_users])

    async def _decline_join(self):
        target_user_data = self.whiteboarding.redis_connector.get_user(self.target_user_id)
        target_user_data["state"] = UserStatus.OUT_ROOM
        target_user_data["room_id"] = None
        self.whiteboarding.redis_connector.update_user(self.target_user_id, target_user_data)
        await self.whiteboarding.get_client_socket(self.target_user_id).send(
            json.dumps({"status": 401, "message": "join declined", "room_id": self.room_id}))
        await self.client_socket.send(json.dumps({"status": 200, "message": "user declined", "uuid": self.uuid}))

    async def _enter_room(self):
        user = self.whiteboarding.redis_connector.get_user(self.user_id)
        user["status"] = UserStatus.QUEUING
        user["room_id"] = self.room_id
        self.whiteboarding.redis_connector.update_user(self.user_id, user)

        host_id = self.whiteboarding.redis_connector.get_host(self.room_id).get("id")
        host_socket = self.whiteboarding.get_client_socket(host_id)
        await host_socket.send(json.dumps({"status": 301, "message": "user in queue", "user_id": self.user_id}))

        await self.client_socket.send(json.dumps({"status": 200, "message": "request sent", "uuid": self.uuid}))
