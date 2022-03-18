from events.constants import EventAction, EventType
from events.whiteboard.whiteboard_event import WhiteboardEvent


class CommentWhiteboardEvent(WhiteboardEvent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = kwargs.get("text")
        self.image_id = kwargs.get("image_id")

    async def handle(self):
        if self.action == EventAction.CREATE:
            self.whiteboarding.redis_connector.insert_event(self.room_id, self.to_dict())
        elif self.action == EventAction.REMOVE:
            self.whiteboarding.redis_connector.remove_event(self.room_id, self.event_id)
        elif self.action == EventAction.EDIT:
            self.whiteboarding.redis_connector.edit_event(self.event_id, self.to_dict())
        await self.redistribute()

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
        if self.action != EventAction.REMOVE and self.image_id is None:
            self.error_msg = "image ID parameter is missing in the payload"
            return False
        if self.action != EventAction.REMOVE and self.text is None:
            self.error_msg = "Comment text parameter is missing in the payload"
            return False
        return True

    def to_dict(self) -> dict:
        parent = super().to_dict()
        parent["text"] = self.text
        parent["image_id"] = self.image_id
        parent['type'] = EventType.COMMENT
        return parent
