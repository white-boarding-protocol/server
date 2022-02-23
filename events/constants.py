from enum import IntEnum


class EventType(IntEnum):
    ROOM = 1
    DRAW = 2
    STICKY_NOTE = 3
    IMAGE = 4
    COMMENT = 5
    UNDO = 6


class EventAction(IntEnum):
    NONE = 1
    CREATE = 2
    EDIT = 3
    REMOVE = 4
