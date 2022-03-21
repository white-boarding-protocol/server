import json

from events.constants import EventAction, EventType
from events.whiteboard.whiteboard_event import WhiteboardEvent


class ImageWhiteboardEvent(WhiteboardEvent):
    SIZE_LIMIT = 7000000

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = kwargs.get("data")  # Encoded data
        self.height = kwargs.get("height")
        self.width = kwargs.get("width")

    async def handle(self):
        if self.action == EventAction.CREATE:
            self.event_id = self.whiteboarding.redis_connector.insert_event(self.room_id, self.to_dict())
        elif self.action == EventAction.REMOVE:
            # Remove image last
            self.whiteboarding.redis_connector.remove_event(self.room_id, self.event_id)
        elif self.action == EventAction.EDIT:
            previous_event = self.whiteboarding.redis_connector.get_event(self.event_id)
            self.data = previous_event["data"]
            self.whiteboarding.redis_connector.edit_event(self.event_id, self.to_dict())
            self.data = None

        await self.client_socket.send(json.dumps({"status": 200, "event": self.to_dict(), "uuid": self.uuid}))
        await self.redistribute_event()

    def is_valid(self) -> bool:
        if self.action is None:
            self.error_msg = "action is missing in the payload"
            return False
        if self.action in [EventAction.EDIT, EventAction.REMOVE] and self.event_id is None:
            self.error_msg = "event_id is missing in the payload"
            return False
        if self.action != EventAction.REMOVE and (self.x_coordinate is None or self.y_coordinate is None):
            self.error_msg = "coordinate is missing in the payload"
            return False
        if self.room_id is None:
            self.error_msg = "room_id parameter is missing in the payload"
            return False
        if self.action == EventAction.CREATE and self.data is None:
            self.error_msg = "image data parameter is missing in the payload"
            return False
        if self.action == EventAction.CREATE and len(self.data) > self.SIZE_LIMIT:
            self.error_msg = f"image is more than {self.SIZE_LIMIT} bytes"
            return False
        return True

    def to_dict(self) -> dict:
        parent = super().to_dict()
        parent["data"] = self.data
        parent['height'] = self.height
        parent['width'] = self.width
        parent['type'] = EventType.IMAGE
        return parent
