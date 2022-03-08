from events.masterevent import MasterEvent


class ServerEvent(MasterEvent):
    def has_perm(self) -> bool:
        return True

    def handle(self) -> list:
        pass

    def is_validate(self) -> bool:
        pass

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = kwargs.get("server_event_type")

    def to_dict(self) -> dict:
        parent = super().to_dict()
        parent["type"] = self.type
        return parent
