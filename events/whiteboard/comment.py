from events.whiteboard.draw import DrawWhiteboardEvent
from events.whiteboard.whiteboard_event import WhiteboardEvent
from events.whiteboard.constants import EventAction, EventType


class CommentWhiteboardEvent(WhiteboardEvent):
    def __init__(self, image_id: str, action: EventAction, text: str = None, draw: DrawWhiteboardEvent = None):
        WhiteboardEvent.__init__(self, EventType.COMMENT, action)
        self.text = text
        self.draw = draw
        self.image_id = image_id
