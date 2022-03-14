from events.whiteboard.whiteboard_event import WhiteboardEvent
import json

class RemoveWhiteboardEvent(WhiteboardEvent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def handle(self):
        self.whiteboarding.redis_connector.remove_event(self.id)

    def is_valid(self) -> bool:
        return True

    def to_dict(self) -> dict:
        parent_dict = super().to_dict()
        return parent_dict

