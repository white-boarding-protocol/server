from events.masterevent import MasterEvent


class WhiteboardEvent(MasterEvent):
    """
    Parent whiteboard event class
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.action = kwargs.get("action")
        self.x_coordinate = kwargs.get("x_coordinate")
        self.y_coordinate = kwargs.get("y_coordinate")
        self.event_id = kwargs.get("event_id")

    def has_perm(self) -> bool:
        return self.user_id in [x.get("id") for x in self.room_users]

    def to_dict(self) -> dict:
        parent = super().to_dict()
        parent["action"] = self.action
        parent["x_coordinate"] = self.x_coordinate
        parent["y_coordinate"] = self.y_coordinate
        parent["event_id"] = self.event_id
        return parent

    async def redistribute(self, redistribute_to):
        return await super().redistribute([user.get("id") for user in self.room_users])
