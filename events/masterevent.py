from abc import abstractmethod
from time import time

import json

from events.constants import EventType, EventAction
from events.exceptions import PermissionDenied
from whiteboarding.whiteboarding import Whiteboarding


class MasterEvent:
    def __init__(self, user_id: str, room_id=None, time_stamp=None):
        self.user_id = user_id
        self.room_id = room_id

        if time_stamp:
            self.time_stamp = time_stamp
        else:
            self.time_stamp = time()

        self.whiteboarding = Whiteboarding()
        self.room_users = None

    @abstractmethod
    def has_perm(self) -> bool:
        pass

    @abstractmethod
    def handle(self):
        pass

    def exec(self):
        if self.has_perm():
            self.handle()
        else:
            raise PermissionDenied()

    @staticmethod
    def deserialize(json_data):
        data = json.loads(json_data)
        event_type = data.pop("type")
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
        elif event_type == EventType.COMMENT:
            from events.whiteboard.comment import CommentWhiteboardEvent
            data["action"] = EventAction(data["action"])
            return CommentWhiteboardEvent(**data)
        elif event_type == EventType.UNDO:
            from events.whiteboard.undo import UndoWhiteboardEvent
            data["action"] = EventAction(data["action"])
            return UndoWhiteboardEvent(**data)

    def redistribute(self):
        pass
