from events.masterevent import MasterEvent
from events.whiteboard.constants import EventType, EventAction


class WhiteboardEvent(MasterEvent):
    """
    Parent whiteboard event class
    """

    def __init__(self, event_type: EventType, event_action=EventAction.NONE):
        super().__init__(1, "2")
        self.type = event_type
        self.action = event_action
