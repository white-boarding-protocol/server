from abc import abstractmethod
from time import time

from events.constants import EventType, EventAction
from events.exceptions import PermissionDenied
from whiteboarding.whiteboarding import Whiteboarding


class MasterEvent:
    def __init__(self, **kwargs):
        self.user_id = kwargs.get("user_id")
        self.room_id = kwargs.get("room_id")
        self.message = kwargs.get("message")

        if kwargs.get("time_stamp"):
            self.time_stamp = kwargs.get("time_stamp")
        else:
            self.time_stamp = time()

        self.whiteboarding = Whiteboarding()
        self._room_users = None

    @property
    def room_users(self):
        if self._room_users is None:
            self._room_users = self.whiteboarding.redis_connector.get_users(self.room_id)
        return self._room_users

    @abstractmethod
    def has_perm(self) -> bool:
        pass

    @abstractmethod
    def handle(self) -> list:
        pass

    def exec(self):
        if self.has_perm():
            redistribute_to = self.handle()
            self._redistribute(redistribute_to)
        else:
            raise PermissionDenied()

    @staticmethod
    def deserialize(data):
        event_type = data.pop("type")
        if event_type is None:
            return MasterEvent(**data)

        if event_type == EventType.ROOM:
            from events.room.room_event import RoomEvent
            return RoomEvent(**data)
        elif event_type == EventType.DRAW:
            from events.whiteboard.draw import DrawWhiteboardEvent
            data["action"] = EventAction(data["action"])
            return DrawWhiteboardEvent(**data)
        elif event_type == EventType.STICKY_NOTE:
            from events.whiteboard.sticky_note import StickyNoteWhiteboardEvent
            data["action"] = EventAction(data["action"])
            return StickyNoteWhiteboardEvent(**data)
        elif event_type == EventType.IMAGE:
            from events.whiteboard.image import ImageWhiteboardEvent
            data["action"] = EventAction(data["action"])
            return ImageWhiteboardEvent(**data)
        elif event_type == EventType.UNDO:
            from events.whiteboard.undo import UndoWhiteboardEvent
            data["action"] = EventAction(data["action"])
            return UndoWhiteboardEvent(**data)

    def _redistribute(self, redistribute_to: list):
        pass

    def to_dict(self) -> dict:
        return {
            "message": self.message,
            "user_id": self.user_id,
            "room_id": self.room_id,
            "time_stamp": self.time_stamp
        }
