from events.whiteboard.constants import EventType, EventAction
from events.whiteboard.whiteboard_event import WhiteboardEvent


class DrawWhiteboardEvent(WhiteboardEvent):

    def __init__(self):
        WhiteboardEvent.__init__(self, EventType.UNDO, EventAction.NONE)
