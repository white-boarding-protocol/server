import json

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
        if self.type in [RoomEventType.ACCEPT_JOIN, RoomEventType.DECLINE_JOIN] and self.target_user_id is None:
            self.error_msg = "target_user is missing in the payload"
            return False
        return True

    async def handle_error(self):
        await self.client_socket.send(json.dumps({"message": self.error_msg, "status": 400}))

    async def _create_room(self) -> list:
        self.room_id = self.whiteboarding.redis_connector.create_room(self.user_id)
        user = {
            "id": self.user_id,
            "state": "in_room",
            "room_id": self.room_id
        }
        self.whiteboarding.redis_connector.insert_user(self.room_id, self.user_id, user)
        await self.client_socket.send(json.dumps({"status": 201, "message": "room created"}))
        return []

    async def _end_room(self) -> list:
        room_users = self.room_users
        for user in room_users:
            user["state"] = "out_room"
            user["room_id"] = None
            self.whiteboarding.redis_connector.update_user(user.get("id"), user)

        self.whiteboarding.redis_connector.remove_room(self.room_id)
        self.client_socket.send(json.dumps({"status": 200, "message": "room ended"}))
        return [x.get("id") for x in room_users]

    async def _leave_room(self) -> list:
        self.whiteboarding.redis_connector.remove_user_from_room(self.room_id, self.user_id)
        current_user_data = self.whiteboarding.redis_connector.get_user(self.user_id)
        current_user_data["state"] = "out_room"
        self.whiteboarding.redis_connector.update_user(self.user_id, current_user_data)
        self.client_socket.send(json.dumps({"status": 200, "message": "left room"}))
        return [x.get("id") for x in self.room_users]

    async def _accept_join(self) -> list:
        self.whiteboarding.redis_connector.insert_user(self.room_id, self.target_user_id)
        room_events = self.whiteboarding.redis_connector.get_events(self.room_id)
        await self.client_socket.send({"status": 200, "events": room_events})
        # TODO not done
        return []

    async def _decline_join(self) -> list:
        target_user_data = self.whiteboarding.redis_connector.get_user(self.target_user_id)
        target_user_data["state"] = "out_room"
        self.whiteboarding.redis_connector.update_user(self.target_user_id, target_user_data)
        self.whiteboarding.get_client_socket(self.target_user_id).send(
            json.dumps({"status": 403, "message": "join declined"}))
        self.client_socket.send(json.dumps({"status": 200, "message": "user declined"}))
        return []

    async def _enter_room(self) -> list:
        # TODO not done
        host_id = self.whiteboarding.redis_connector.get_host(self.room_id)
        host_socket = self.whiteboarding.get_client_socket(host_id)
        host_socket.send()
        return [host_id]
