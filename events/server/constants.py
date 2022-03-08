from enum import IntEnum


class ServerEventType(IntEnum):
    USER_CONNECT = 0
    USER_DISCONNECT = 1
