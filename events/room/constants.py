from enum import IntEnum


class RoomEventType(IntEnum):
    CREATE_ROOM = 0
    USER_JOIN = 1
    USER_LEAVE = 2
    END_ROOM = 3
    ACCEPT_JOIN = 4
    DECLINE_JOIN = 5
