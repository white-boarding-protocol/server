class PermissionDenied(Exception):
    def __init__(self, user):
        super().__init__(f"{user} does is not allowed for this operation")
