from events.whiteboard.whiteboard_event import WhiteboardEvent

from services.redis_connector import RedisConnector

class StickyNoteWhiteboardEvent(WhiteboardEvent):
    def __init__(self, text: str, **kwargs):
        super().__init__(**kwargs)
        self.text = text

    def has_perm(self) -> bool:
        users = self.room_users
        return self.user_id in users

    def handle(self):
        return self.whiteboarding.redis_connector.insert_event(self.room_id, vars(self))