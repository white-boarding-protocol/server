from events.constants import EventType
from events.whiteboard.whiteboard_event import WhiteboardEvent


class UndoWhiteboardEvent(WhiteboardEvent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def handle(self):
        last_event_id = self.whiteboarding.redis_connector.get_last_event_id(self.room_id)
        self.whiteboarding.redis_connector.remove_event(last_event_id)
        await self.redistribute_event()

    def is_valid(self) -> bool:
        return True

    def to_dict(self) -> dict:
        parent_dict = super().to_dict()
        parent_dict['type'] = EventType.UNDO
        return parent_dict
