from events.whiteboard.whiteboard_event import WhiteboardEvent


class UndoWhiteboardEvent(WhiteboardEvent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
