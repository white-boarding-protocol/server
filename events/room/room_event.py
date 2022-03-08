from events.masterevent import MasterEvent


class RoomEvent(MasterEvent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = kwargs.get("event_type")
        self.target_user = kwargs.get("target_user")
