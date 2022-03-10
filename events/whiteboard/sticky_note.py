from events.whiteboard.whiteboard_event import WhiteboardEvent


# TODO Sep

class StickyNoteWhiteboardEvent(WhiteboardEvent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = kwargs.get("text")

    def handle(self):
        return self.whiteboarding.redis_connector.insert_event(self.room_id, vars(self))
