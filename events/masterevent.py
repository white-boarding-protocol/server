from time import time


class MasterEvent:
    def __init__(self, event_type, user_id: str, session_id=None, time_stamp=None):
        self.user_id = user_id
        self.type = event_type
        self.session_id = session_id

        if time_stamp:
            self.time_stamp = time_stamp
        else:
            self.time_stamp = time()
