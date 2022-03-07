from events.masterevent import MasterEvent
from events.constants import EventAction


class WhiteboardEvent(MasterEvent):
    """
    Parent whiteboard event class
    """

    def __init__(self, action: EventAction = EventAction.NONE, **kwargs):
        super().__init__(**kwargs)
        self.action = action
