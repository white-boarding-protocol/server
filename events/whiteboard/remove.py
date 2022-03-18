from events.constants import EventType
from events.whiteboard.whiteboard_event import WhiteboardEvent


class RemoveWhiteboardEvent(WhiteboardEvent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def handle(self):
        self.whiteboarding.redis_connector.remove_event(self.id)
        await self.redistribute()

    def is_valid(self) -> bool:
        return True

    def to_dict(self) -> dict:
        parent_dict = super().to_dict()
        parent_dict["type"] = EventType.REMOVE
        return parent_dict
