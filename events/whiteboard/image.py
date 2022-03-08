from events.whiteboard.whiteboard_event import WhiteboardEvent


class ImageWhiteboardEvent(WhiteboardEvent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
