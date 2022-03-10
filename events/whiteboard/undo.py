from events.whiteboard.whiteboard_event import WhiteboardEvent


# TODO Bipin

class UndoWhiteboardEvent(WhiteboardEvent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
