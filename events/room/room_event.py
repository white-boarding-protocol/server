from events.masterevent import MasterEvent


class RoomEvent(MasterEvent):
    def __init__(self, event_type, target_user: str):
        super().__init__()
        self.type = event_type
        self.target_user = target_user
