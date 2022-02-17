from EventConstants import EventType, EventAction


class Event:
    """
    Parent event class
    """
    type: EventType
    action: EventAction

    def __init__(self, event_type, event_action=EventAction.NONE):
        self.type = event_type
        self.action = event_action
