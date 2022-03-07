from events.whiteboard.whiteboard_event import WhiteboardEvent


class StickyNoteWhiteboardEvent(WhiteboardEvent):
    def __init__(self, text: str, **kwargs):
        super().__init__(**kwargs)
        self.text = text
