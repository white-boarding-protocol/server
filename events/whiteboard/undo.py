from events.whiteboard.whiteboard_event import WhiteboardEvent


class UndoWhiteboardEvent(WhiteboardEvent):

    def __init__(self, **kwargs):
        if kwargs.get("action"):
            kwargs.pop("action")
        super().__init__(**kwargs)
