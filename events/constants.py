from enum import IntEnum


class EventType(IntEnum):
    SERVER = 0
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
    REMOVE = 2 # todo: does this action occur once we add REMOVE as event type?
