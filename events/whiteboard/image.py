from events.whiteboard.whiteboard_event import WhiteboardEvent
from events.whiteboard.constants import EventAction, EventType


class ImageWhiteboardEvent(WhiteboardEvent):
    def __init__(self, text: str, action: EventAction):
        WhiteboardEvent.__init__(self, EventType.IMAGE, action)
        self.text = text
