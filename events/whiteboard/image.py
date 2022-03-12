from events.whiteboard.whiteboard_event import WhiteboardEvent


# TODO Sam, handle all different actions for your event

class ImageWhiteboardEvent(WhiteboardEvent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
