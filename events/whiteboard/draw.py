from events.whiteboard.constants import EventAction, EventType
from events.whiteboard.whiteboard_event import WhiteboardEvent


class DrawWhiteboardEvent(WhiteboardEvent):

    def __init__(self, action: EventAction):
        WhiteboardEvent.__init__(self, EventType.DRAW, action)
