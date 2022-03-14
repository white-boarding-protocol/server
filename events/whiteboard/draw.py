from events.constants import EventAction
from events.whiteboard.whiteboard_event import WhiteboardEvent
import json

# TODO Sam, handle all different actions for your event


class DrawWhiteboardEvent(WhiteboardEvent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = kwargs.get("color")
        self.tool = kwargs.get("tool")
        self.width = kwargs.get("width")

    def to_dict(self) -> dict:
        parent = super().to_dict()
        parent["color"] = self.color
        parent["tool"] = self.tool
        parent["width"] = self.width
        return parent

    def handle(self) -> list:
        if self.action == EventAction.CREATE:
            self.whiteboarding.redis_connector.insert_event(self.room_id, self.to_dict())
        elif self.action == EventAction.REMOVE:
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
        if self.color is None:
            self.error_msg = "color parameter is missing in the payload"
            return False
        if self.width is None:
            self.error_msg = "width parameter is missing in the payload"
            return False
        if self.tool is None:
            self.error_msg = "tool parameter is missing in the payload"
            return False
        return True