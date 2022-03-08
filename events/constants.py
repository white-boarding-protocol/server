from enum import IntEnum


class EventType(IntEnum):
    SERVER = 0
    ROOM = 1
    DRAW = 2
    STICKY_NOTE = 3
    IMAGE = 4
    COMMENT = 5
    UNDO = 6


class EventAction(IntEnum):
    NONE = 0
    CREATE = 1
    EDIT = 2
    REMOVE = 3
