from enum import Enum


class EventType(Enum):
    DRAW = 1
    STICKY_NOTE = 2
    IMAGE = 3
    COMMENT = 4
    UNDO = 5


class EventAction(Enum):
    NONE = 1
    CREATE = 2
    EDIT = 3
    REMOVE = 4
