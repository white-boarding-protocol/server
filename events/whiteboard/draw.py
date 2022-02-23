from events.whiteboard.whiteboard_event import WhiteboardEvent


class DrawWhiteboardEvent(WhiteboardEvent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
