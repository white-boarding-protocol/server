import json

from events.whiteboard.whiteboard_event import WhiteboardEvent


class StickyNoteWhiteboardEvent(WhiteboardEvent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = kwargs.get("text")
        self.error_msg = None

    def handle(self):
        self.whiteboarding.redis_connector.insert_event(self.room_id, self.to_dict())
        return self.room_users

    def is_valid(self) -> bool:
        if self.room_id is None:
            self.error_msg = "room_id parameter is missing in the payload"
            return False
        if self.text is None:
            self.error_msg = "text parameter is missing in the payload"
            return False
        return True

    async def handle_error(self):
        await self.client_socket.send(json.dumps({"message": self.error_msg, "status": 400}))

    def to_dict(self) -> dict:
        parent_dict = super().to_dict()
        parent_dict["text"] = self.text
        return parent_dict
