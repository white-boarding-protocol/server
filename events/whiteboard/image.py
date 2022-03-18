from events.constants import EventAction, EventType
from events.whiteboard.whiteboard_event import WhiteboardEvent


class ImageWhiteboardEvent(WhiteboardEvent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = kwargs.get("data")  # Encoded data

    async def handle(self):
        if self.action == EventAction.CREATE:
            self.whiteboarding.redis_connector.insert_event(self.room_id, self.to_dict())
        elif self.action == EventAction.REMOVE:
            # Remove all comments first
            comment_ids = [x.get("event_id") for x in self.whiteboarding.redis_connector.get_room_events(self.room_id)
                           if x.get("type") == EventType.COMMENT and x.get("image_id") == self.event_id]
            for comment_id in comment_ids:
                self.whiteboarding.redis_connector.remove_event(self.room_id, comment_id)
            # Remove image last
            self.whiteboarding.redis_connector.remove_event(self.room_id, self.event_id)
        await self.redistribute()

    def is_valid(self) -> bool:
        if self.action is None:
            self.error_msg = "action is missing in the payload"
            return False
        if self.action == EventAction.EDIT:
            self.error_msg = "edit not allowed for image"
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
        if self.action != EventAction.REMOVE and self.data is None:
            self.error_msg = "image data parameter is missing in the payload"
            return False
        return True

    def to_dict(self) -> dict:
        parent = super().to_dict()
        parent["data"] = self.data
        parent['type'] = EventType.IMAGE
        return parent
