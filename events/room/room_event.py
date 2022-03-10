from events.masterevent import MasterEvent


# TODO Sep

class RoomEvent(MasterEvent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = kwargs.get("room_event_type")
        self.target_user = kwargs.get("target_user")

    def to_dict(self) -> dict:
        parent = super().to_dict()
        parent["type"] = self.type
        parent["target_user"] = self.target_user
        return parent
