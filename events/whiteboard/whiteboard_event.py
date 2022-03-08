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

    def has_perm(self) -> bool:
        users = self.room_users
        return self.user_id in users

    def handle(self) -> list:
        return []

    def to_dict(self) -> dict:
        parent = super().to_dict()
        parent["action"] = self.action
        parent["x_coordinate"] = self.x_coordinate
        parent["y_coordinate"] = self.y_coordinate
        return parent
