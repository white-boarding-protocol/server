from events.whiteboard.draw import DrawWhiteboardEvent
from events.whiteboard.whiteboard_event import WhiteboardEvent


class CommentWhiteboardEvent(WhiteboardEvent):
    def __init__(self, image_id: str, text: str = None, draw: DrawWhiteboardEvent = None, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.draw = draw
        self.image_id = image_id
