import json

from events.constants import EventType
from events.whiteboard.whiteboard_event import WhiteboardEvent


class UndoWhiteboardEvent(WhiteboardEvent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_event_id = None

    async def handle(self):
        self.last_event_id = self.whiteboarding.redis_connector.get_last_event_id(self.room_id)
        self.whiteboarding.redis_connector.remove_event(self.room_id, self.last_event_id)
        await self.client_socket.send(json.dumps({"status": 200, "event": self.to_dict(), "uuid": self.uuid}))
        await self.redistribute_event()

    def is_valid(self) -> bool:
        return True

    def to_dict(self) -> dict:
        parent_dict = super().to_dict()
        parent_dict['type'] = EventType.UNDO
        parent_dict['last_event_id'] = self.last_event_id
        return parent_dict
