from events.masterevent import MasterEvent
from events.room.constants import RoomEventType
from whiteboarding.whiteboarding import Whiteboarding


class RoomEvent(MasterEvent):
    def __init__(self, event_type: RoomEventType, target_user: str, **kwargs):
        print(kwargs)
        super().__init__(**kwargs)
        self.type = event_type
        self.target_user = target_user
