from events.whiteboard.whiteboard_event import WhiteboardEvent
import json

class RemoveWhiteboardEvent(WhiteboardEvent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def handle(self):
        self.whiteboarding.redis_connector.remove_event(self.id)

    def is_valid(self) -> bool:
        return True

    async def handle_error(self):
        await self.client_socket.send(json.dumps({"message": self.error_msg, "status": 400}))

    def to_dict(self) -> dict:
        parent_dict = super().to_dict()
        return parent_dict

