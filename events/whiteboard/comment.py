from events.constants import EventAction
from events.whiteboard.whiteboard_event import WhiteboardEvent


class CommentWhiteboardEvent(WhiteboardEvent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = kwargs.get("text")
        self.image_id = kwargs.get("image_id")

    async def handle(self):
        if self.action == EventAction.CREATE:
            self.whiteboarding.redis_connector.insert_event(self.room_id, self.to_dict())
            image_event = self.whiteboarding.redis_connector.get_event(self.image_id)
            image_event.comments.append(self.event_id)  # Add the new comment to the image
            self.whiteboarding.redis_connector.edit_event(self.room_id, image_event)  # Edit the image associated
        elif self.action == EventAction.REMOVE:
            self.whiteboarding.redis_connector.remove_event(self.room_id, self.event_id)
            image_event = self.whiteboarding.redis_connector.get_event(self.image_id)
            image_event.comments.remove(self.event_id)  # remove the comment from the image
            self.whiteboarding.redis_connector.edit_event(self.room_id, image_event)  # Edit the image associated
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
        if self.x_coordinate is None or self.y_coordinate is None:
            self.error_msg = "coordinate is missing in the payload"
            return False
        if self.room_id is None:
            self.error_msg = "room_id parameter is missing in the payload"
            return False
        if self.image_id is None:
            self.error_msg = "image ID parameter is missing in the payload"
            return False
        if self.text is None:
            self.error_msg = "Comment text parameter is missing in the payload"
            return False
        return True

    def to_dict(self) -> dict:
        parent = super().to_dict()
        parent["text"] = self.text
        parent["image"] = self.image_id
        return parent
