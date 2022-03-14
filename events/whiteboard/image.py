from events.constants import EventAction
from events.whiteboard.whiteboard_event import WhiteboardEvent
import json

# TODO Sam, handle all different actions for your event

class ImageWhiteboardEvent(WhiteboardEvent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = kwargs.get("data") # Encoded data
        self.ls_comment_id = kwargs.get("comments") 
        # List of comments event ids that is attached to the image
        # This last can be empty but it cannot be missing

    def handle(self) -> list:
        if self.action == EventAction.CREATE:
            self.whiteboarding.redis_connector.insert_event(self.room_id, self.to_dict())
        elif self.action == EventAction.REMOVE:
            # Remove all comments first
            for comment_id in self.ls_comment_id:
                self.whiteboarding.redis_connector.remove_event(self.room_id, comment_id)
            # Remove image last
            self.whiteboarding.redis_connector.remove_event(self.room_id, self.event_id)
        elif self.action == EventAction.EDIT:
            self.whiteboarding.redis_connector.edit_event(self.event_id, self.to_dict())
        return [x.get("id") for x in self.room_users]

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
        if self.data is None:
            self.error_msg = "image data parameter is missing in the payload"
            return False
        if self.ls_comment_id is None:
            self.error_msg = "comments list parameter is missing in the payload"
            return False
        return True

    def to_dict(self) -> dict:
        parent = super().to_dict()
        parent["data"] = self.data
        parent["comments"] = self.ls_comment_id
        return parent
