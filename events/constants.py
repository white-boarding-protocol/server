from enum import IntEnum


class EventType(IntEnum):
    ROOM = 1
    DRAW = 2
    STICKY_NOTE = 3
    IMAGE = 4
    COMMENT = 5
    UNDO = 6
    REMOVE = 7


class EventAction(IntEnum):
    CREATE = 0
    EDIT = 1
    REMOVE = 2


class UserStatus(IntEnum):
    IN_ROOM = 0
    OUT_ROOM = 1
    QUEUING = 2
