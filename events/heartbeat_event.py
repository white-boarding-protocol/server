from events.masterevent import MasterEvent


class HeartBeatEvent(MasterEvent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def has_perm(self) -> bool:
        return True

    async def handle(self):
        return

    def is_valid(self) -> bool:
        return True
