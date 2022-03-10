from events.whiteboard.whiteboard_event import WhiteboardEvent


# TODO Sam
class ImageWhiteboardEvent(WhiteboardEvent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
