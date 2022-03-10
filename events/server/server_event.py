import json

from events.exceptions import InvalidEvent
from events.server.constants import ServerAction


class ServerEvent:
    def __init__(self, client_socket, msg, action: ServerAction, whiteboarding):
        self.action = action
        self.msg = msg
        self.client_socket = client_socket
        self.whiteboarding = whiteboarding

    def is_msg_valid(self):
        return self.msg.get("user_id") is not None

    async def exec(self):
        if self.is_msg_valid():
            user_id = self.msg.get("user_id")
            if self.action == ServerAction.USER_CONNECT:
                self.whiteboarding.add_online_user(user_id, self.client_socket)
                await self.whiteboarding.get_client_socket(user_id).send(json.dumps({"msg": "hello_ack"}))
            elif self.action == ServerAction.USER_DISCONNECT:
                self.whiteboarding.remove_online_user(user_id)
                await self.whiteboarding.get_client_socket(user_id).send(json.dumps({"msg": "abort_ack"}))
        else:
            raise InvalidEvent()
