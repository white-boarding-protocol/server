import json

from events.constants import EventAction, EventType
from events.whiteboard.whiteboard_event import WhiteboardEvent


class DrawWhiteboardEvent(WhiteboardEvent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = kwargs.get("color")
        self.tool = kwargs.get("tool")
        self.coordinates = kwargs.get("coordinates")
        self.width = kwargs.get("width")

    def to_dict(self) -> dict:
        parent = super().to_dict()
        parent["color"] = self.color
        parent["coordinates"] = self.coordinates
        parent["tool"] = self.tool
        parent["width"] = self.width
        parent['type'] = EventType.DRAW
        return parent

    async def handle(self):
        if self.action == EventAction.CREATE:
            self.event_id = self.whiteboarding.redis_connector.insert_event(self.room_id, self.to_dict())
        elif self.action == EventAction.REMOVE:
            self.whiteboarding.redis_connector.remove_event(self.room_id, self.event_id)
        elif self.action == EventAction.EDIT:
            self.whiteboarding.redis_connector.edit_event(self.event_id, self.to_dict())
        await self.client_socket.send(json.dumps({"status": 200, "event": self.to_dict(), "uuid": self.uuid}))
        await self.redistribute_event()

    def is_valid(self) -> bool:
        if self.action is None:
            self.error_msg = "action is missing in the payload"
            return False
        if self.action in [EventAction.EDIT, EventAction.REMOVE] and self.event_id is None:
            self.error_msg = "event_id is missing in the payload"
            return False
        if self.action != EventAction.REMOVE and self.coordinates is None:
            self.error_msg = "coordinates is missing in the payload"
            return False
        if self.room_id is None:
            self.error_msg = "room_id parameter is missing in the payload"
            return False
        return True
