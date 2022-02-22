from events.whiteboard.whiteboard_event import WhiteboardEvent
from events.whiteboard.constants import EventAction, EventType


class StickyNoteWhiteboardEvent(WhiteboardEvent):
    def __init__(self, text: str, action: EventAction):
        WhiteboardEvent.__init__(self, EventType.STICKY_NOTE, action)
        self.text = text
