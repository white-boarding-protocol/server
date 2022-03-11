class PermissionDenied(Exception):
    def __init__(self, user):
        super().__init__(f"{user} does is not allowed for this operation")


class InvalidEvent(Exception):
    def __init__(self):
        super().__init__("Invalid Event")


class Disconnected(Exception):
    def __init__(self):
        super().__init__("User has disconnected")
