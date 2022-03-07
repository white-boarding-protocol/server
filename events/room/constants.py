from enum import IntEnum


class RoomEventType(IntEnum):
    USER_JOIN = 1
    USER_LEAVE = 2
    END_ROOM = 3
    ACCEPT_JOIN = 4
    DECLINE_JOIN = 5
